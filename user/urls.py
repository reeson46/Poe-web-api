from django.urls import path
from . import views

urlpatterns = [
    path('', views.characterList, name='character'),
    path("api/", views.characterDetail, name="charcter-detail")
]
