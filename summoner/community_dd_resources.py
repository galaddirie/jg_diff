from summoner.id_translation import *
DRAGON = 'https://raw.communitydragon.org/latest/plugins/'
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