from django.urls import path
from filemanager import views

urlpatterns = [
    path(route='index', view=views.index, name="filemanager_index"),
    path(route='folder_list', view=views.folder_list, name="folder_list"),
    path(route='show_folder', view=views.show_folder, name="show_folder"),

]