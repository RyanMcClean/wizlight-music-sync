from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('toggleBulb/', views.toggleBulb, name='toggle'),
    path('queryBulb/', views.queryBulb, name='query'),
    path('colorBulb/', views.colorBulb, name='color')
]
