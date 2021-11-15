from django.db import models

# Create your models here.

# class SummonerAccount(models.Model):
#     accountId	string
#     profileIconId	int
#     revisionDate	long
#     summonerName	string
#     summonerId	string	
#     puuid	string	
#     summonerLevel	long


# # make a field that connects PromotionInfo to something in SummonerRankedInfo
# class SummonerRankedInfo(models.Model):
#     leagueId	string	
#     summonerId	string
#     summonerName	string	
#     queueType	string	
#     tier	string	
#     rank	string	
#     leaguePoints	int	
#     wins	int	Winning team on Summoners Rift.
#     losses	int	Losing team on Summoners Rift.
#     hotStreak	boolean

# class PromotionInfo(models.Model):
#     losses	int	
#     progress	string	
#     target	int	
#     wins	int

# # MAKE SOMETHING THAT POINTS MATCHLIST TO MATCH REFRENCE TO MATCH

# class MatchList(models.Model):
#     startIndex	int	
#     totalGames	int	
#     endIndex	int	
#     matches	List[MatchReferenceDto]	

# class MatchReference(models.Model):
#     gameId	long	
#     role	string	
#     season	int	
#     platformId	string	
#     champion	int	
#     queue	int	
#     lane	string	
#     timestamp	long


# class Match(models.Model):
#      gameId = models.BigIntegerField()	
#      role = models.CharField(max_length=32)	
#      season = models.IntegerField()	
#      platformId  = models.CharField(max_length=32)		
#      champion = models.IntegerField()	
#      queue	= models.IntegerField()	
#      lane = models.CharField(max_length=32)		
#      timestamp =	models.BigIntegerField()