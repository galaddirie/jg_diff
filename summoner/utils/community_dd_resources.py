from summoner.utils.id_translation import *
CDRAGON = 'https://raw.communitydragon.org/latest/plugins/'


def get_perstige_crest(level):
    crest_id = border_icon_id(level)
    icon = CDRAGON+'rcp-fe-lol-static-assets/global/default/images/uikit/themed-level-ring/theme-{}-solid-border.png'\
        .format(crest_id)
    #print('Making call:', icon)
    return icon


def get_rank_icon(tier):
    ranked_id = ranked_icon_id(tier)
    icon = CDRAGON+'rcp-fe-lol-static-assets/global/default/images/ranked-mini-regalia/{}.png'\
        .format(ranked_id)
    #print('Making call:', icon)
    return get_ranked_armor(tier)  # icon


def get_ranked_armor(tier):
    ranked_id = ranked_icon_id(tier)
    if ranked_id == 'unranked' or ranked_id == 'provisional':
        return "https://raw.communitydragon.org/latest/plugins/rcp-fe-lol-profiles/global/default/profile_unranked.png"
    icon = f"https://raw.communitydragon.org/latest/game/assets/ux/tftmobile/particles/tft_regalia_{ranked_id}.png"
    return icon


def get_rank_banner(tier):
    ranks = 'unranked,iron,bronze,silver,gold,platinum,diamond,master,grandmaster,challenger'.split(
        ',')
    i = str(ranks.index(tier)).zfill(2)
    icon = 'https://raw.communitydragon.org/latest/game/assets/loadouts/regalia/banners/{}_{}_banner.png'\
        .format(i, tier)
    #print('Making call:', icon)
    return "https://raw.communitydragon.org/latest/game/assets/loadouts/regalia/banners/00_unranked_banner.csscraps.png"  # icon
