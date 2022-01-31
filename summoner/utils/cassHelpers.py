from typing import Dict
from jg_diff.settings import CASSIOPEIA_RIOT_API_KEY
import json
import arrow
from django.http import HttpRequest
import requests
from django_cassiopeia import cassiopeia as cass
import datapipelines

from summoner.utils.id_translation import *
from summoner.utils.community_dd_resources import *


def get_participant_data(match, player, details_expanded=False):
    """
    Helper for get_match()
    """
    player_data = {}

    items = []
    for item in player.stats.items:
        try:
            items.append({'name': item.name, 'image': item.image.url, 'desc': item.description,
                         'id': item.id, 'cost': item.gold})  # 'desc': item.description,
        except AttributeError:
            items.append(None)
    trinket = items.pop(-1)

    cs = player.stats.total_minions_killed + player.stats.neutral_minions_killed
    seconds = match.duration.total_seconds()
    cs_per_minute = round(cs/((seconds % 3600) // 60), 1)

    keystone = ''

    try:
        for rune in player.runes:
            if rune.is_keystone:
                primary_tree = rune.path.name
                keystone = rune
            elif rune.path.name != primary_tree:
                secondary_tree = rune.path
        runes = [{'image': keystone.image.url, 'name': keystone.name},
                 {'image': secondary_tree.image_url, 'name': secondary_tree.name}]
    except datapipelines.common.NotFoundError:
        runes = []

    try:
        spells = [
            {'name': player.summoner_spell_d.name,
                'image': player.summoner_spell_d.image.url},
            {'name': player.summoner_spell_f.name, 'image': player.summoner_spell_f.image.url}]
    except datapipelines.common.NotFoundError:
        spells = []

    rank = ' '
    # NOTE with this attribute we would be making a call to the api
    # for every player in the match looking at their league entry,
    # at the current moment rather than their league entry at that instance
    # a solution for this would be to store
    # players and matches in the database and
    """
    try:    
        if False:
            solo_rank = 'Level ' + str(player.summoner.level)
            player_entries = player.summoner.league_entries
            for league in player_entries:
                if match.queue.name == 'ranked_solo_fives' or match.queue.name == 'ranked_flex_fives':
                    if league.queue.name == match.queue.name:
                        solo_rank =league.tier.value.capitalize()+' '+league.division.value
                else:
                    if player_entries.fives.tier.value.lower() != 'unranked':
                         solo_rank =player_entries.fives.tier.value.capitalize()+' '+player_entries.fives.division.value               
    except:
       ...
    """
    player_data = {
        'id': player.summoner.id,
        'name': player.summoner.name,
        'level': player.stats.level,

        'role': '',
        'kills': player.stats.kills,
        'deaths': player.stats.deaths,
        'assists': player.stats.assists,
        'KDA': '{}/{}/{}'.format(player.stats.kills, player.stats.deaths, player.stats.assists),
        'kill_ratio': '{}:1'.format(round(player.stats.kda, 2)),
        'multi_kill': num_to_multikill(player.stats.largest_multi_kill),
        'damage': "{:,}".format(player.stats.total_damage_dealt_to_champions),
        'damage_literal': int(player.stats.total_damage_dealt_to_champions),
        'damage_percentage': '',
        'vision_score': player.stats.vision_score,
        'cs': cs,
        'csm': cs_per_minute,
        'rank': rank,
        'wards_placed': player.stats.wards_placed,
        'wards_killed': player.stats.wards_killed,
        'control_wards': player.stats.vision_wards_placed,
        'champion': {'name': player.champion.name, 'image': player.champion.image.url},
        'spells': spells,
        'runes': runes,
        'items': items,
        'trinket': trinket,
        'teams': [player.team.side.name, player.enemy_team.side.name],
        # 'roles':player.role
    }
    return player_data


def get_match(match_id, continent, puuid, details_expanded=False):
    match = cass.Match(id=match_id, continent=continent)

    match.load()

    try:
        is_remake = match.is_remake
    except AttributeError:
        is_remake = False

    seconds = match.duration.total_seconds()
    minutes = str(int((seconds % 3600) // 60)).zfill(2)
    seconds = str(int(seconds % 60)).zfill(2)
    duration = [minutes, seconds]
    creation = humanize_time(arrow.utcnow() - match.creation)

    match_info = {
        'is_remake': is_remake,
        'duration': '{}:{}'.format(duration[0], duration[1]),
        'creation': creation,
        'queue': queue_to_string(match.queue.value),
        'tier_average': 'not implemented'
    }
    summoner = None
    participants = {}
    max_damage = 0

    # THIS ENTIRE TEAM SECTION IS BAD, BUT Is It BETTER THAN HAVE DUPLICATE HTML? yes

    for team in match.teams:
        players = {}
        for player in team.participants:
            player_data = {}

            if player.summoner.puuid == puuid:

                player_data = get_participant_data(
                    match, player, details_expanded)
                summoner = player
                summoner_stats = player_data
            else:
                if not details_expanded:

                    player_data = {
                        'name': player.summoner.name,
                        'champion': {'name': player.champion.name, 'image': player.champion.image.url},
                    }
                else:
                    player_data = get_participant_data(
                        match, player, details_expanded)
            try:
                if player_data['damage_literal'] > max_damage:
                    max_damage = player_data['damage_literal']
            except KeyError:
                pass
            players[player_data['name']] = player_data

        participants[team.side.name] = players

    teams = [
        [summoner_stats['teams'][0], participants[summoner_stats['teams'][0]]],
        [summoner_stats['teams'][1], participants[summoner_stats['teams'][1]]]
    ]

    if summoner:
        if summoner.stats.win:
            match_info['win'] = 'WIN'
        else:
            match_info['win'] = 'LOSE'
        if match_info['is_remake']:
            match_info['win'] = 'REMAKE'

    match_data = {
        'id': match_id,  # we will
        'match_info': match_info,
        'summoner_info': summoner_stats,
        'participants': participants,
        'teams': teams,
        'max_damage': max_damage
    }
    return match_data


def get_match_history(puuid: str, continent: str, start: int):

    url = 'https://{}.api.riotgames.com/lol/match/v5/matches/by-puuid/{}/ids?&start={}&count={}'\
        .format(continent.lower(), puuid, start, 5)
    headers = {"X-Riot-Token": CASSIOPEIA_RIOT_API_KEY}

    r = requests.get(url, headers=headers)
    print('Making Call:', url)
    match_history = []
    match_summary = stats = {
        'num': 0,
        'wins': 0,
        'loses': 0,
        'kills': 0,
        'deaths': 0,
        'assists': 0,
        'roles': [],  # [{role:'', image:'', wins:0, loses:0}],
        'champions': {},  # {'name':'', 'image':'', 'wins':0, 'loses':0}
    }
    for match_id in json.loads(r.text):
        match = get_match(match_id, cass.data.Continent(continent), puuid)
        match_summary['num'] += 1
        match_summary['kills'] += match['summoner_info']['kills']
        match_summary['deaths'] += match['summoner_info']['deaths']
        match_summary['assists'] += match['summoner_info']['assists']

        champion = match['summoner_info']['champion']
        if champion['name'] not in match_summary['champions']:
            match_summary['champions'][champion['name']] = {
                'name': champion['name'],
                'image': champion['image'],
                'wins': 0,
                'loses': 0,
                'kills': 0,
                'deaths': 0,
                'assists': 0,
            }
        match_summary['champions'][champion['name']
                                   ]['kills'] += match['summoner_info']['kills']
        match_summary['champions'][champion['name']
                                   ]['deaths'] += match['summoner_info']['deaths']
        match_summary['champions'][champion['name']
                                   ]['assists'] += match['summoner_info']['assists']
        if match['match_info']['win'] == 'WIN':
            match_summary['wins'] += 1
            match_summary['champions'][champion['name']]['wins'] += 1
        if match['match_info']['win'] == 'LOSE':
            match_summary['loses'] += 1
            match_summary['champions'][champion['name']]['loses'] += 1
        match_history.append(match)
    return match_history, match_summary


def get_league_entry(league: cass.League) -> Dict:
    icon = get_rank_icon(league.tier.name)
    banner = get_rank_banner(league.tier.name)
    promo = []
    promo_not_played = []
    if league.promos:
        promo = league.promos.progress
        promo_not_played = range(league.promos.not_played)
    entry = {
        'rank': league.tier.value.capitalize()+' '+league.division.value,
        'icon': icon,
        'banner': banner,
        'lp': league.league_points,
        'wins': league.wins,
        'losses': league.losses,
        'WR': round(league.wins/(league.wins+league.losses)*100, 1),
        'hot': league.hot_streak,
        'promos': {'played': promo, 'not_played': promo_not_played},
        'league_name': league.league,
    }
    return entry


def get_summoner_helper(request: HttpRequest) -> Dict:
    summoner_data = {}
    region = request.GET['region']
    name = request.GET['username']
    # removes all whitespace from names ex. hello world is the same name as helloworld
    # replaces the joined the room text so players can copy paste from game lobbies

    names = " ".join(name.split()).replace('joined the room.', ',').split(',')
    name_check = []
    i = 0
    for player in names:
        summoner = cass.get_summoner(name=player, region=region)
        if summoner.exists:
            # TODO do not make a api request for match history here, rather load match history after page is loaded
            # maybe we check the cache for a match list here and if none is in cache, we make the request,
            # unless we hit update where we then make a new api request and add it to the cache
            # get_match_history(summoner.sanitized_name, summoner.puuid, summoner.region.continent.value, 0)
            match_history = {}
            leagues = {'SOLO': {'rank': 'Unranked', 'icon': get_rank_icon('provisional'), 'banner': get_rank_banner('unranked')},
                       'FLEX': {'rank': 'Unranked', 'icon': get_rank_icon('provisional'), 'banner': get_rank_banner('unranked')}}
            k = 0

            league_entries = summoner.league_entries
            for entry in league_entries:
                try:
                    if entry.queue.name == 'ranked_solo_fives':
                        leagues['SOLO'] = get_league_entry(entry)
                    if entry.queue.name == 'ranked_flex_fives':
                        leagues['FLEX'] = get_league_entry(entry)
                except ValueError:
                    continue

            data = {
                'continent': summoner.region.continent.value,
                'name': summoner.name,
                'puuid': summoner.puuid,
                'region': region,
                'level': summoner.level,
                'match_history': match_history,
                'leagues': leagues,
                'profile_icon': summoner.profile_icon.url,
                'profile_icon_border': get_perstige_crest(summoner.level),
            }
            if summoner.sanitized_name not in name_check:
                summoner_data[i] = data
                name_check.append(summoner.sanitized_name)
                i += 1
    return summoner_data
