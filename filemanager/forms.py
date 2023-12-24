from django import forms

class AddFolderForm(forms.Form): 
    foldername = forms.CharField(label="Nama Folder", max_length = 255, help_text = "Masukkan Nama Folder")
    slug = forms.CharField(widget = forms.HiddenInput(), max_length = 255)
    year = forms.CharField(widget = forms.HiddenInput(), max_length = 4)
    folder = forms.CharField(widget = forms.HiddenInput(), max_length = 255)


class RenameFileForm(forms.Form): 
    newname = forms.CharField(label="Nama File/Folder", max_length = 255, help_text = "Masukkan Nama File/Folder")
    slug = forms.CharField(widget = forms.HiddenInput(), max_length = 255)
    year = forms.CharField(widget = forms.HiddenInput(), max_length = 4)
    folder = forms.CharField(widget = forms.HiddenInput(), max_length = 255)
    filename = forms.CharField(widget = forms.HiddenInput(), max_length = 255)
