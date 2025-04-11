from django.urls import path
from . import views
from . import variables

urlpatterns = [
    path("", views.index, name="index"),
    path("discover/", views.discover, name="discover"),
    path("toggleBulb/", views.toggle_bulb, name="toggle"),
    path("queryBulb/", views.query_bulb, name="query"),
    path("colorBulb/", views.color_bulb, name="color"),
    path("activateSync/", views.activate_music_sync, name="music-sync"),
    path("stopSync/", views.stop_audio_sync, name="stop-music-sync"),
    path("crud/", views.crud, name="crud"),
    path("delete/<str:ip>", views.delete_bulb, name="delete"),
    path("clearError/", views.clear_error, name="clear-error"),
    path("faq/", views.faqs, name="faq"),
    path("about/", views.about, name="about"),
]
