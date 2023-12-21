from django.urls import path
from filemanager import views

urlpatterns = [
    path(route='index', view=views.index, name="index"),
]