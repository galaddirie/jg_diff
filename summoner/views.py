from typing import Match
from jg_diff.settings import CASSIOPEIA_RIOT_API_KEY
from summoner.id_translation import *
import json
import arrow
from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, response
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.views.decorators.csrf import ensure_csrf_cookie
import requests
from django_cassiopeia import cassiopeia as cass

DRAGON = 'https://raw.communitydragon.org/latest/plugins/'

# MATCH HISORY HELPERS


def get_participant_data(match, player):
    """
    Helper for get_match()
    """
    player_data = {}
    
    rank_data =[]
    if match.game_type == 'ranked':
        rank = player.summoner.ranks[match.queue]
        rank_data=[rank.tier.value,rank.division.value]
    
    items =[]
    for item in player.stats.items:
        trinket ={'name':'', 'image': ''}
        try: 
            
            items.append({'name': item.name,'image':item.image.url,'desc': sanitize_desc(item.description), 'id':item.id}) # 'desc': item.description,
    
        except:
            ...
    trinket = items.pop(-1)
    items += [None]*(6-len(items))

    cs = player.stats.total_minions_killed + player.stats.neutral_minions_killed    
    seconds = match.duration.total_seconds()    
    cs_per_minute = round(cs/((seconds % 3600) // 60),1)

    keystone = ''
    for rune in player.runes:
        if rune.is_keystone:
            primary_tree= rune.path.name
            keystone = rune
        elif rune.path.name != primary_tree:
            secondary_tree = rune.path
    multi_kill = num_to_multikill(player.stats.largest_multi_kill)
    solo_rank = 'UNRANKED'
    for league in player.summoner.league_entries:
        try:
            if league.queue.name == 'ranked_solo_fives':
                solo_rank =league.tier.value.capitalize()+' '+league.division.value
            else:
                solo_rank = 'UNRANKED'
        except:
            ...


    player_data={
        'id':player.summoner.id,
        'name': player.summoner.name,
        'level': player.stats.level,
        'role': '',
        'kills': player.stats.kills,
        'deaths': player.stats.deaths,
        'assists': player.stats.assists,
        'KDA': '{}/{}/{}'.format(player.stats.kills, player.stats.deaths, player.stats.assists),
        'kill_ratio':'{}:1'.format( round(player.stats.kda,2)),
        'multi_kill': multi_kill,
        
        'vision_score': player.stats.vision_score,
        'cs': cs,
        'csm': cs_per_minute,
        'rank': solo_rank,

        'champion':{'name':player.champion.name, 'image':player.champion.image.url},
        'spells': [{'name':player.summoner_spell_d.name,'image':player.summoner_spell_d.image.url}, 
        {'name':player.summoner_spell_f.name,'image':player.summoner_spell_f.image.url}],
        'runes': [{'image':keystone.image.url, 'name':keystone.name}, 
                  {'image': secondary_tree.image_url, 'name': secondary_tree.name}
                 ],
        'items': items,
        'trinket':trinket
    }
    return player_data



def get_match(match_id, continent, name):
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
    participants =[]
    tier_acc = []
    for team in match.teams:
        players = {}
        # we should only initially load for main player unless player clicks on more details
        for player in team.participants:
            player_data = {}
            
            player_data = get_participant_data(match,player)
            players[player_data['name']] = player_data
            if player.summoner.name == name:
                summoner = player
                summoner_stats = player_data
                    
            
        participants.append(players)

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
        'participants': participants
    }
    return match_data


def get_match_history(name, puuid, continent,start):
    
    url_response = requests.get('https://{}.api.riotgames.com/lol/match/v5/matches/by-puuid/{}/ids?&start={}&count={}&api_key={}'
                                .format(continent.lower(), puuid, start, 1, CASSIOPEIA_RIOT_API_KEY))
    print(url_response)
    match_history = []
   # print(json.loads(url_response.text))
    for match_id in json.loads(url_response.text):
        
        match = get_match(match_id, cass.data.Continent(continent), name)
        match_history.append(match)
        
        
    
    
    return match_history


def get_recent_info(match_history):
    for match in match_history:

        info = {
            'history': match_history,
            'games': len(match_history),
            'wins': match_history,

        }
    return []


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
            # check if it is ajax
            match_history = get_match_history(summoner.name, summoner.puuid, summoner.region.continent.value, 0)
            match_info = get_recent_info(match_history)
            #
            leagues = {'SOLO': {'rank': 'Unranked', 'icon': get_rank_icon('unranked'), 'banner': get_rank_banner('unranked')},
                       'FLEX': {'rank': 'Unranked', 'icon': get_rank_icon('unranked'), 'banner': get_rank_banner('unranked')}}
            k = 0
            for league in summoner.league_entries:

                if league.queue.name == 'ranked_solo_fives':
                    leagues['SOLO'] = get_league_entry(league)
                if league.queue.name == 'ranked_flex_fives':
                    leagues['FLEX'] = get_league_entry(league)
            data = {
                'continent':summoner.region.continent.value,
                'name': summoner.name,
                'puuid': summoner.puuid,
                'region':region,
                'level': summoner.level,
                'rank': summoner.ranks,
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

    if is_ajax:
        
        
        name = request.GET.get('username',None)
        puuid = request.GET.get('puuid',None)
        continent = request.GET.get('continent',None)
        start = request.GET.get('start',None)
        
        match_history = get_match_history(name, puuid, continent, int(start))
        rendered = render_to_string('summoner/match_history.html', {0:{'match_history': match_history}})
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
