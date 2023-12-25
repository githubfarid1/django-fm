from django.urls import path
from filemanager import views

urlpatterns = [
    path(route='index', view=views.index, name="filemanager_index"),
    path(route='folder_list', view=views.folder_list, name="folder_list"),
    path(route='show_folder', view=views.show_folder, name="show_folder"),
    path(route='download', view=views.download, name='download'),
    path(route='remove_file', view=views.remove_file, name="remove_file"),
    path(route='download_folder', view=views.download_folder, name="download_folder"),
    path(route='rename_file', view=views.rename_file, name="rename_file"),
    path(route='add_folder', view=views.add_folder, name="add_folder"),
    path(route='upload_file', view=views.upload_file, name="upload_file"),


]