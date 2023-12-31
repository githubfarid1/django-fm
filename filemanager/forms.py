from django import forms

class AddFolderForm(forms.Form): 
    foldername = forms.CharField(label="Nama Folder", max_length = 255, help_text = "Masukkan Nama Folder")
    folder = forms.CharField(widget = forms.HiddenInput(), max_length = 255)


class RenameFileForm(forms.Form): 
    newname = forms.CharField(label="Nama File/Folder", max_length = 255, help_text = "Masukkan Nama File/Folder")
    folder = forms.CharField(widget = forms.HiddenInput(), max_length = 255)
    filename = forms.CharField(widget = forms.HiddenInput(), max_length = 255)
