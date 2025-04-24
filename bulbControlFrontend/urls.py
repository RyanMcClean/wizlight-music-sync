from django.urls import path, re_path
from . import views
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # URLS for views
    path("", views.index, name="index"),
    path("crud/", views.crud, name="crud"),
    path("about/", views.about, name="about"),
    path("faq/", views.faqs, name="faq"),
    # URLS for bulb control
    path("discover/", views.discover, name="discover"),
    path("toggleBulb/", views.toggle_bulb, name="toggle"),
    path("queryBulb/", views.query_bulb, name="query"),
    path("colorBulb/", views.color_bulb, name="color"),
    # URLS for database operations
    path("delete/<str:ip>", views.delete_bulb, name="delete"),
    path("edit/<str:ip>", views.edit_bulb, name="edit"),
    # URLS for error and success messages
    path("clearSuccess/", views.clear_success, name="clear-success"),
    path("clearError/", views.clear_error, name="clear-error"),
    # URLS for music sync
    path("activateSync/", views.activate_music_sync, name="music-sync"),
    path("stopSync/", views.stop_audio_sync, name="stop-music-sync"),
    # This allows for serving of static files when DEBUG is False (i.e. in production)
    re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
