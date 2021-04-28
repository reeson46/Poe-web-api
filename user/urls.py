from django.urls import path
from . import views

urlpatterns = [
    path('', views.charactersAndTabs, name='character-list-and-tabs'),
    path('api/character_detail/', views.characterDetail, name='charcter-detail'),
    path('api/stashtab/', views.stashTab, name='stash-tab')
]
