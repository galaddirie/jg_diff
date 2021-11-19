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

def queue_to_string(queue):
    ids = {
    "RANKED_SOLO_5x5": 'Ranked Solo',  
    "NORMAL_5V5_BLIND_PICK": 'Normal', 
    "TEAM_BUILDER_DRAFT_UNRANKED_5x5":'Normal', 
    "RANKED_FLEX_SR":'Ranked Flex',  
    "ARAM": 'ARAM',  
    "NORMAL_3X3_BLIND_PICK" : '3v3 Blind', 
    
    "CLASH":'Clash',  
    "BOT_3X3_INTERMEDIATE":'Bots',  
    "BOT_3X3_INTRO":'Intro Bots',  
    "BOT_3X3_BEGINNER":'Beginner Bots',  
    "BOT_5X5_INTRO":'Intro Bots',  
    "BOT_5X5_BEGINNER" : 'Beginner Bots', 
    "BOT_5X5_INTERMEDIATE": 'Intermediate Bots',  
    "ARURF_5X5": 'URF', 

    "TUTORIAL_1": 'TUTORIAL', 
    "TUTORIAL_2" :'TUTORIAL', 
    "TUTORIAL_3":'TUTORIAL',
    }
    if queue in ids:
        return ids[queue]
    return queue