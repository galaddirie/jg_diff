from jg_diff.settings import CASSIOPEIA_RIOT_API_KEY

import json
import arrow
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, response
from django.template.loader import render_to_string
import requests
from django_cassiopeia import cassiopeia as cass


from summoner.id_translation import *
from summoner.community_dd_resources import *

# MATCH HISORY HELPERS


def get_participant_data(match, player, details_expanded=False):
    """
    Helper for get_match()
    """
    player_data = {}

    items =[]
    for item in player.stats.items:
        try:
            items.append({'name': item.name,'image':item.image.url,'desc': item.description, 'id':item.id, 'cost':item.gold}) # 'desc': item.description,
        except:
            items.append(None)
    trinket = items.pop(-1)

    cs = player.stats.total_minions_killed + player.stats.neutral_minions_killed    
    seconds = match.duration.total_seconds()    
    cs_per_minute = round(cs/((seconds % 3600) // 60),1)


    keystone = ''
    runes = []
    try:
        for rune in player.runes:
            if rune.is_keystone:
                primary_tree= rune.path.name
                keystone = rune
            elif rune.path.name != primary_tree:
                secondary_tree = rune.path
        runes = [{'image':keystone.image.url, 'name':keystone.name}, 
                  {'image': secondary_tree.image_url, 'name': secondary_tree.name}]
    except:
        ...
    spells = []
    try:
        spells = [{'name':player.summoner_spell_d.name,'image':player.summoner_spell_d.image.url}, 
        {'name':player.summoner_spell_f.name,'image':player.summoner_spell_f.image.url}]
    except:
        ...

    solo_rank = ' '
    try:    
        if False:
            solo_rank = 'Level ' + str(player.summoner.level)
            player_entries = player.summoner.league_entries
            for league in player_entries:
                print(league)
                if match.queue.name == 'ranked_solo_fives' or match.queue.name == 'ranked_flex_fives':
                    if league.queue.name == match.queue.name:
                        solo_rank =league.tier.value.capitalize()+' '+league.division.value
                else:
                    if player_entries.fives.tier.value.lower() != 'unranked':
                         solo_rank =player_entries.fives.tier.value.capitalize()+' '+player_entries.fives.division.value               
    except:
        ...

    player_data={
        'id':player.summoner.id,
        'name': player.summoner.name,
        'level': player.stats.level,
        'role': '',
        'iklls': player.stats.kills,
        'deaths': player.stats.deaths,
        'assists': player.stats.assists,
        'KDA': '{}/{}/{}'.format(player.stats.kills, player.stats.deaths, player.stats.assists),
        'kill_ratio':'{}:1'.format( round(player.stats.kda,2)),
        'multi_kill': num_to_multikill(player.stats.largest_multi_kill),
        'damage':"{:,}".format(player.stats.total_damage_dealt_to_champions),
        'damage_literal':int(player.stats.total_damage_dealt_to_champions),
        'damage_percentage':'',
        'vision_score': player.stats.vision_score,
        'cs': cs,
        'csm': cs_per_minute,
        'rank': solo_rank,
        'wards_placed':player.stats.wards_placed,
        'wards_killed':player.stats.wards_killed,
        'control_wards':player.stats.vision_wards_placed,
        'champion':{'name':player.champion.name, 'image':player.champion.image.url},
        'spells': spells,
        'runes': runes,
        'items': items,
        'trinket':trinket,
        'teams':[player.team.side.name, player.enemy_team.side.name]
    }
    return player_data


def get_match(match_id, continent, name, details_expanded=False):
    match = cass.Match(id=match_id, continent=continent)
    
    match.load()
    
    try:
        is_remake = match.is_remake
    except:
        is_remake = False

    seconds = match.duration.total_seconds()    
    minutes = str(int((seconds % 3600) // 60)).zfill(2)
    seconds = str(int(seconds % 60)).zfill(2)
    duration = [minutes,seconds]
    creation = humanize_time(arrow.utcnow() - match.creation)
    
    match_info = {
        'is_remake': is_remake,
        'duration': '{}:{}'.format(duration[0],duration[1]),
        'creation': creation,
        'queue': queue_to_string(match.queue.value),
        'tier_average':'not implemented'
    }
    summoner = None
    participants = {}
    max_damage = 0

    # THIS ENTIRE TEAM SECTION IS BAD, BUT Is It BETTER THAN HAVE DUPLICATE HTML? yes 
    for team in match.teams:
        players = {}
        for player in team.participants:
            player_data = {}
            if player.summoner.sanitized_name == name:
                player_data = get_participant_data(match,player,details_expanded)       
                summoner = player
                summoner_stats = player_data        
            else:
                if not details_expanded:

                    player_data = {
                        'name': player.summoner.name, 
                        'champion':{'name':player.champion.name, 'image':player.champion.image.url},
                    }
                else:
                    player_data = get_participant_data(match,player,details_expanded)
            try:
                if player_data['damage_literal'] > max_damage:
                    max_damage= player_data['damage_literal']  
            except:
                ...
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
        'id':match_id, # we will 
        'match_info': match_info,
        'summoner_info': summoner_stats,
        'participants': participants,
        'teams': teams,
        'max_damage': max_damage
    }
    return match_data


def get_match_history(name, puuid, continent,start):
    
    url = 'https://{}.api.riotgames.com/lol/match/v5/matches/by-puuid/{}/ids?&start={}&count={}'\
        .format(continent.lower(), puuid, start, 1)
    headers = { "X-Riot-Token": CASSIOPEIA_RIOT_API_KEY}

    r = requests.get(url, headers=headers)
    print('GETTING MATCH HISTORY FROM API', r.text)
    match_history = []
    for match_id in json.loads(r.text):
        print(match_id)
        match = get_match(match_id, cass.data.Continent(continent), name)
        match_history.append(match)
    return match_history

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
        summoner = cass.get_summoner(name=player, region=region)
        if summoner.exists:
            # TODO do not make a api request for match history here, rather load match history after page is loaded
            # maybe we check the cache for a match list here and if none is in cache, we make the request, 
            # unless we hit update where we then make a new api request and add it to the cache
            match_history = {} #get_match_history(summoner.sanitized_name, summoner.puuid, summoner.region.continent.value, 0)
            leagues = {'SOLO': {'rank': 'Unranked', 'icon': get_rank_icon('unranked'), 'banner': get_rank_banner('unranked')},
                       'FLEX': {'rank': 'Unranked', 'icon': get_rank_icon('unranked'), 'banner': get_rank_banner('unranked')}}
            k = 0
            
            league_entries = summoner.league_entries
            for entry in league_entries:
                try:
                    entry.queue
                except:
                    continue
                if entry.queue.name == 'ranked_solo_fives':
                    leagues['SOLO'] = get_league_entry(entry)
                if entry.queue.name == 'ranked_flex_fives':
                    leagues['FLEX'] = get_league_entry(entry)
            
            data = {
                'continent':summoner.region.continent.value,
                'name': summoner.name,
                'puuid': summoner.puuid,
                'region':region,
                'level': summoner.level,
                'match_history': match_history,
                'leagues': leagues,
                'profile_icon': summoner.profile_icon.url,
                'profile_icon_border': get_perstige_crest(summoner.level),
            }
            #print(data)
            if summoner.sanitized_name not in name_check:
                summoner_data[i] = data
                name_check.append(summoner.sanitized_name)
                i += 1
    return summoner_data


def get_summoner(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    name = request.GET.get('username',None)
    region = request.GET.get('region',None)
    santized_name = ''.join(name.lower().split())
    
    if is_ajax:
        if (request.GET.get('details_expand',None)):
            match_id = request.GET.get('id',None)
            continent = request.GET.get('continent',None)
            details = get_match(match_id, continent, santized_name, request.GET.get('details_expand',None))
            rendered = render_to_string('summoner/match_details.html', {'match': details, 'region':region,'name':name})
            
        if (request.GET.get('start',None)):
            puuid = request.GET.get('puuid',None)
            continent = request.GET.get('continent',None)
            start = request.GET.get('start',None)
            match_history = get_match_history(santized_name, puuid, continent, int(start))
            rendered = render_to_string('summoner/match_card.html', {0:{'match_history': match_history ,'name':name, 'region':region}})

        return HttpResponse(rendered)
 
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