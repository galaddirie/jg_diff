# from __future__ import division
# from os import kill
# from django.db import models
# from django_cassiopeia import cassiopeia as cass


# # from summoner.id_translation import *
# # from summoner.community_dd_resources import *
# # # # Create your models here.


# class Summoner(models.Model):
#     name = models.CharField(max_length=16)
#     puuid = models.CharField(unique=True, max_length=78)
#     summoner_id = models.CharField(max_length=63)
#     region = models.CharField(max_length=78)
#     level = models.IntegerField()
#     profile_icon = models.ImageField(
#         default='', null=True, upload_to='summoner_icons')

#     def get_summoner():
#         ...

#     def get_ranks():
#         ...

#     def get_match_history():
#         ...


# class LeagueEntries(models.Model):
#     summoner = models.ForeignKey(Summoner, on_delete=models.CASCADE)
#     season = models.CharField(max_length=12)
#     tier = models.CharField(max_length=12)
#     division = models.IntegerField()
#     lp = models.IntegerField()
#     history = models.TextField()

#     def save(self, *args, **kwargs) -> None:
#         ...
#        # return super().save(*args, **kwargs)


# class Match(models.Model):
#     match_id = models.CharField(max_length=32)
#     duration = models.DurationField()
#     creation = models.DateTimeField()
#     queue = models.CharField(max_length=32)

#     def get_participants():
#         ...

#     def get_teams():
#         ...

#     def is_blue_team(participant):
#         ...


# class Participant(models.Model):
#     summoner = models.ForeignKey(Summoner, on_delete=models.CASCADE)
#     match = models.ForeignKey(Match, on_delete=models.CASCADE)
#     team = models.CharField(max_length=4)
#     champion = models.CharField(max_length=16)
#     kills = models.IntegerField()
#     deaths = models.IntegerField()
#     assists = models.IntegerField()
#     max_multi_kill = models.IntegerField()
#     damage = models.IntegerField()
#     vision_score = models.IntegerField()
#     cs = models.IntegerField()
