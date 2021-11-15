def get_region_ids(i):

    ids ={
        "BR":'BR1',
        "EUNE":'EUN1',
        "EUW":'EUWBR1',
        "JP":'JP1',
        "KR":'KR1',
        "LAN":'LA1',
        "LAS":'LA2',
        "NA":'NA1',
        "OCE":'OC1',
        "TR":'TR1',
        "RU":'RU'
    }

    return ids[i]

# QUEUE_IDS = {
    
# }

def border_icon_id(level):
    levels = [1,30,50,75,100,125,150,175,200,225,250,275,300,325,350,375,400,425,450,475,500]
    for i in range(len(levels)):
        if level < levels[i] and i !=0:
            return i
    if level >=500:
        return '21'
    return'1'

def ranked_icon_id(tier):
    return tier