from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("toggleBulb/", views.toggle_bulb, name="toggle"),
    path("queryBulb/", views.query_bulb, name="query"),
    path("colorBulb/", views.color_bulb, name="color"),
    path("activateMusic/", views.activate_music_sync, name="music-sync"),
]
