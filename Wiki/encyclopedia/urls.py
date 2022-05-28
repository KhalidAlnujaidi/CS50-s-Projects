from django.urls import path

from . import views
from entries import*

urlpatterns = [
    path("wiki", views.index, name="index"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("wiki/<str:entry>/edit", views.edit, name="edit"),
    path("search", views.search, name="search"),
    path("create", views.create, name="create"),
    path("save",views.save, name="save"),
    path("random", views.random, name="random")
    
]
