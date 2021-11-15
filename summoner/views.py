from typing import Match
from jg_diff.settings import CASSIOPEIA_RIOT_API_KEY
from summoner.id_translation import *

from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, response
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator

import requests
from django_cassiopeia import cassiopeia as cass

DRAGON = 'https://raw.communitydragon.org/latest/plugins/'

# MATCH HISORY HELPERS


def get_match(match_id, continent, name):
    match = cass.Match(id=match_id, continent=continent)
    print(match.exists)
    if match.exists:
        summoner = None
        for player in match.participants:
            if player.summoner.name == name:
                summoner = player

        if summoner:
            stats = {
                'items': summoner.stats.items,
                'kills': summoner.stats.kills,
                'deaths': summoner.stats.deaths,
                'assists': summoner.stats.assists,
                'kda': summoner.stats.kda,
                'level': summoner.stats.level,
                'win': summoner.stats.win,
            }

            summoner_info = {
                'champion': summoner.champion,
                'stats': stats,
                'side': summoner.side,

            }

            game = {
                'player': summoner_info,
                'blue_team': match.blue_team.participants,
                'red_team': match.red_team.participants,
                'is_remake': match.is_remake,
                'win': summoner_info['stats']['win'],
                'duration': match.duration,
                'creation': match.creation,
                'queue': match.queue,
            }
        return game
    return match


def get_match_history(summoner, start):
    continent = summoner.region.continent.value.lower()
    region_id = get_region_ids(summoner.region.value)
    puuid = summoner.puuid
    print(puuid)
    # queue={}
    url_response = requests.get('https://{}.api.riotgames.com/lol/match/v5/matches/by-puuid/{}/ids?&start={}&api_key={}'
                                .format(continent, puuid, start, CASSIOPEIA_RIOT_API_KEY))

    match_history = []
    mh_temp = "".join(url_response.text.split()).replace(
        region_id + '_', '').split(',')
    for match_id in mh_temp:
        acc = ''
        for char in match_id:
            if char.isdigit():
                acc += char
        match = acc  # get_match(acc, summoner.region.continent, summoner.name)
        match_history.append(match)

    return match_history


def get_recent_info(match_history):
    for match in match_history:

        info = {
            'history': match_history,
            'games': len(match_history),
            'wins': match_history,

        }
    return match_history


# RESOURCES GETTERS
def get_perstige_crest(level):
    crest_id = border_icon_id(level)
    icon = DRAGON+'rcp-be-lol-game-data/global/default/content/src/leagueclient/prestigeborders/theme-{}-solid-border.png'\
        .format(crest_id)
    return icon


def get_rank_icon(tier):
    ranked_id = ranked_icon_id(tier)
    icon = DRAGON+'rcp-fe-lol-static-assets/global/default/images/ranked-mini-regalia/{}.png'\
        .format(ranked_id)
    return icon


def get_rank_banner(tier):
    ranks = 'unranked,iron,bronze,silver,gold,platinum,diamond,master,grandmaster,challenger'.split(
        ',')
    i = str(ranks.index(tier)).zfill(2)
    icon = 'https://raw.communitydragon.org/latest/game/assets/loadouts/regalia/banners/{}_{}_banner.png'\
        .format(i, tier)
    return icon

# LEAGUE ENTRY HELPER


def get_league_entry(league):
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


def get_summoner_helper(request):

    summoner_data = {}

    region = request.GET['region']
    name = request.GET['username']
    # removes all whitespace from names ex. hello world is the same name as helloworld
    # replaces the joined the room text so players can copy paste from game lobbies

    names = " ".join(name.split()).replace('joined the room.', ',').split(',')
    name_check = []
    i = 0
    for player in names:
        summoner = cass.Summoner(name=player, region=region)
        if summoner.exists:
            # begin_time=cass.Patch.latest(region="NA").start
            # begin_index=0, end_index=21

            match_history = get_match_history(summoner, 0)
            match_info = get_recent_info(match_history)
            leagues = {'SOLO': {'rank': 'Unranked', 'icon': get_rank_icon('unranked'), 'banner': get_rank_banner('unranked')},
                       'FLEX': {'rank': 'Unranked', 'icon': get_rank_icon('unranked'), 'banner': get_rank_banner('unranked')}}
            k = 0
            for league in summoner.league_entries:

                if league.queue.name == 'ranked_solo_fives':
                    leagues['SOLO'] = get_league_entry(league)
                if league.queue.name == 'ranked_flex_fives':
                    leagues['FLEX'] = get_league_entry(league)
            data = {
                'name': summoner.name,
                'level': summoner.level,
                'rank': summoner.ranks,
                'match history': match_info,
                'leagues': leagues,
                'profile_icon': summoner.profile_icon.url,
                'profile_icon_border': get_perstige_crest(summoner.level),
            }
            print(data)
            if summoner.sanitized_name not in name_check:
                summoner_data[i] = data
                name_check.append(summoner.sanitized_name)
                i += 1
    return summoner_data


def get_summoner(request):

    # empty name
    if request.GET['username'] == '':
        return render(request, 'summoner/player_page_empty.html')

    summoner_data = get_summoner_helper(request)
    # invalid / DNE in selected region name goes here
    if not summoner_data:
        return render(request, 'summoner/player_page_invalid.html', summoner_data)

    if len(summoner_data) > 1:  # multi
        return get_multi(request, summoner_data)

    return render(request, 'summoner/player_page_valid.html', summoner_data)


def get_multi(request, summoner_data=None):
    return render(request, 'summoner/multi.html', summoner_data)


def home(request):
    return render(request, 'summoner/home.html')


def construction(request):
    return render(request, 'construction.html')
