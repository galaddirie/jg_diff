from enum import Enum
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
    'ULTIMATE_SPELLBOOK':'Ultimates',
    "TUTORIAL_1": 'TUTORIAL', 
    "TUTORIAL_2" :'TUTORIAL', 
    "TUTORIAL_3":'TUTORIAL',


    }
    if queue in ids:
        return ids[queue]
    return queue
def sanitize_desc(desc):
    acc = ''
    isTag = False
    for char in desc:
        if char == '<':
            isTag = True
        if char == '>':
            isTag = False
            acc += ' '
        elif not isTag:
            acc += char
    return acc

def humanize_time(time):
    days = time.days # Get Day 
    hours,remainder = divmod(time.seconds,3600) # Get Hour 
    minutes,seconds = divmod(remainder,60) # Get Minute & Second 
    ans = ''
    if days <= 0:
        if hours > 0:
            ans += '{} hours '.format(hours)
        elif minutes > 0:
            ans += '{} minutes '.format(minutes)
        else:
            ans = '{} seconds '.format(seconds)
    else:
        ans = '{} days '.format(days)
    ans += 'ago'
    return ans

def num_to_multikill(num):
    multi_kills = [None, None,'Double', 'Triple', 'Quadra', 'Penta'] 
    
    return multi_kills[num]

