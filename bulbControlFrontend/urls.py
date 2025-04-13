from django.urls import path, re_path
from . import views
from django.views.static import serve 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    path("discover/", views.discover, name="discover"),
    path("toggleBulb/", views.toggle_bulb, name="toggle"),
    path("queryBulb/", views.query_bulb, name="query"),
    path("colorBulb/", views.color_bulb, name="color"),
    path("activateSync/", views.activate_music_sync, name="music-sync"),
    path("stopSync/", views.stop_audio_sync, name="stop-music-sync"),
    path("crud/", views.crud, name="crud"),
    path("crud/<str:success>", views.crud_success, name="crud_success"),
    path("delete/<str:ip>", views.delete_bulb, name="delete"),
    path("clearError/", views.clear_error, name="clear-error"),
    path("clearSuccess/", views.clear_success, name="clear-success"),
    path("faq/", views.faqs, name="faq"),
    path("about/", views.about, name="about"),
    path("edit/<str:ip>", views.edit_bulb, name="edit"),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT})
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
