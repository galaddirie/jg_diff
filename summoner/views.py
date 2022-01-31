from typing import Dict

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse, response
from django.template.loader import render_to_string


from summoner.utils.cassHelpers import *
# MATCH HISORY HELPERS


def get_summoner(request: HttpRequest) -> HttpResponse:
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    name = request.GET.get('username', None)
    region = request.GET.get('region', None)
    santized_name = ''.join(name.lower().split())

    if is_ajax:
        if (request.GET.get('details_expand', None)):  # client is requesting specificmatch
            match_id = request.GET.get('id', None)
            continent = request.GET.get('continent', None)
            puuid = request.GET.get('puuid', None)
            details = get_match(match_id, continent, puuid,
                                request.GET.get('details_expand', None))
            rendered = render_to_string(
                'summoner/match_details.html', {'match': details, 'region': region, 'name': name})
            data = {'matchCard': rendered}
        if (request.GET.get('start', None)):  # client is requesting match_history
            puuid = request.GET.get('puuid', None)
            continent = request.GET.get('continent', None)
            start = request.GET.get('start', None)
            match_data = get_match_history(puuid, continent, int(start))
            match_history, summary = match_data[0], match_data[1]
            rendered = render_to_string(
                'summoner/match_card.html', {0: {'match_history': match_history, 'name': name, 'region': region}})
            data = {'history': rendered, 'summary': summary}
        return JsonResponse(data)
    else:
        if request.GET['username'] == '':
            return render(request, 'summoner/player_page_empty.html')

        summoner_data = get_summoner_helper(request)

        if not summoner_data:
            # invalid / DNE in selected region name goes here
            return render(request, 'summoner/player_page_invalid.html', summoner_data)

        if len(summoner_data) > 1:
            # multi
            return get_multi(request, summoner_data)

        return render(request, 'summoner/player_page_valid.html', summoner_data)


def get_multi(request: HttpRequest, summoner_data: Dict = None) -> HttpResponse:
    return render(request, 'summoner/multi.html', summoner_data)


def home(request: HttpRequest) -> HttpResponse:
    return render(request, 'summoner/home.html')


def construction(request: HttpRequest) -> HttpResponse:
    return render(request, 'construction.html')
