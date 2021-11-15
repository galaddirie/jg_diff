from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name ='summoner-home'),
    path('summoner/', views.get_summoner, name ='player-page'),
    path('construction/', views.construction, name ='construction'),
    path('multi/', views.get_multi, name ='multi'),
    # path('login/', views.login, name ='construction'),
]
