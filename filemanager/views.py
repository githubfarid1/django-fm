from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.views.decorators.csrf import csrf_exempt
import os, shutil
from django.conf import settings
from datetime import date, datetime
import mimetypes
from os.path import exists
import json
from .forms import AddFolderForm, RenameFileForm
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from urllib.parse import urlencode

def index(request):
    return HttpResponse("tess")

def build_breadcrumbs(url):
    folderlist = []
    if url != '':
        folderlist = str(url).split(os.path.sep )
    result = []
    for idx, folder in enumerate(folderlist):
        tmpl = []
        for i in range(0, idx+1):
            tmpl.append(folderlist[i])
        mdict = {
            'label': folder,
            'link': os.path.sep.join(tmpl),
        }
        result.append(mdict)
    result.insert(0, {"label":'Root', 'link':'~'})
    result[-1]['link'] = ''
    return result

@csrf_exempt
def show_folder(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    username = request.user.username
    folder = request.GET.get("folder")
    if folder == None:
        base_url = reverse('show_folder')
        query_string =  urlencode({'folder': ''})
        url = '{}?{}'.format(base_url, query_string)
        return redirect(url)
    context = {
        'username': username,
        'breadcrumbs': build_breadcrumbs(folder),
        'folder': folder,
    }
    return render(request=request, template_name='filemanager/show_folder.html', context=context)


@csrf_exempt
def folder_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    folder = request.GET.get("folder")
    # if folder == 'None':
    #     folder = ""
    
    username = request.user.username
    folderlist = str(folder).split("/")
    folderlist.pop(0)
    path = os.path.join(settings.FM_LOCATION, username, folder)
    contents =os.listdir(path)
    data = []
    for file in contents:
        if os.path.isfile(os.path.join(path, file)):
            filemime, filesize, filetype, mime_type, mtime = get_fileinfo(os.path.join(path, file))
            icon_location = os.path.join('assets/filetypes', filemime)
            data.append({
                'name': file,
                'type': 'file',
                'icon_location': icon_location,
                'filesize': filesize,
                'filetype': filetype,
                'mimetype': mime_type,
                'folder': folder,
                'mtime': datetime.fromtimestamp(mtime),
                
            })
        else:
            mtime = os.path.getmtime(os.path.join(path, file))
            data.append({
                'name': file,
                'type': 'folder',
                'link': os.path.join(folder, file),
                'mtime': datetime.fromtimestamp(mtime),
                
            })
    
    # dep = Department.objects.get(slug=slug)        
    context = {
        'data': data,
        'folder': folder,
        'showfolderurl': 'fm_pjpa_show_folder',
        'downloadurl': 'fm_pjpa_download',
        # 'slug': slug,
        # 'year': year,
        'zipfolderurl':'fm_pjpa_download_folder',
        'renameurl': 'fm_pjpa_rename_file',
        'removeurl': 'fm_pjpa_remove_file',
        
}
    # return HttpResponse(context)
    return render(request=request, template_name='filemanager/folder_list.html', context=context)

def get_fileinfo(filepath):
    file_size = os.path.getsize(filepath)
    unit = 'bytes'
    if file_size < 90000000:
        unit = 'kb'
    elif file_size < 900000000:
        unit = 'mb'
    elif file_size < 9000000000:
        unit = 'gb'
    # print(file_size)    
    exponents_map = {'bytes': 0, 'kb': 1, 'mb': 2, 'gb': 3}
    if unit not in exponents_map:
        raise ValueError("Must select from \
        ['bytes', 'kb', 'mb', 'gb']")
    else:
        size = file_size / 1024 ** exponents_map[unit]
        file_size = round(size, 2)
    
    filesizestr = f"{str(file_size)} {unit}"    
    
    mime_type, encoding = mimetypes.guess_type(filepath)
    # print(mime_type)
    mtime = os.path.getmtime(filepath)
    if mime_type != None:
        if 'pdf' in mime_type:
            filemime, filetype = 'pdf.png', 'PDF'
        elif 'excel' in mime_type:
            filemime, filetype = 'excel.png', 'Excel'
        elif 'sheet' in mime_type:
            filemime, filetype = 'excel.png', 'Excel'
        elif 'png' in mime_type:
            filemime, filetype = 'image.png', 'Image'
        elif 'jpg' in mime_type:
            filemime, filetype = 'image.png', 'Image'
        elif 'jpeg' in mime_type:
            filemime, filetype = 'image.png', 'Image'
        elif 'mp3' in mime_type:
            filemime, filetype = 'sound.png', 'Image'
        elif 'video' in mime_type:
            filemime, filetype = 'video.png', 'Video'
        elif 'powerpoint' in mime_type:
            filemime, filetype = 'ppt.png', 'Power Point'
        elif  'presentation' in mime_type:
            filemime, filetype = 'ppt.png', 'Power Point'
        elif 'wordprocessingml' in mime_type:
            filemime, filetype = 'doc.png', 'Word'
        elif 'msword' in mime_type:
            filemime, filetype = 'doc.png', 'Word'
        elif 'compressed' in mime_type:
            filemime, filetype = 'zip.png', 'Zip'
        elif 'zip' in mime_type:
            filemime, filetype = 'zip.png', 'Zip'
        else:
            filemime, filetype = 'unknown.png', 'Unknown'
    else:
        filemime, filetype = 'unknown.png', 'Unknown'
                
    return filemime, filesizestr, filetype, mime_type, mtime


@csrf_exempt
def remove_file(request):
    if request.method == "POST":
        filename = request.POST.get('filename')
        folder = request.POST.get("folder")
        type = request.POST.get("type")

        path = os.path.join(settings.FM_LOCATION, request.user.username, folder, filename)
        if exists(path):
            if type=='file':
                os.remove(path)
            else:
                shutil.rmtree(path)
            message = f"Hapus { type } {filename} Sukses."
        else:
            message = f"Hapus { type } {filename} Gagal."
                    
        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                    "movieListChanged": None,
                    "showMessage": message
                })
            })
    else:
        folder = request.GET.get("folder")
        filename = request.GET.get("filename")
        type = request.GET.get("type")
        
    return render(request, 'filemanager/remove_file.html', {
        'folder': folder,
        'filename': filename,
        'type': type
    })

def zipfolder(path):
    return shutil.make_archive((path, "zip", path))
        
@csrf_exempt
def download_folder(request):
    if request.method == "POST":
        filename = request.POST.get('filename')
        folder = request.POST.get("folder")

        path = os.path.join(settings.FM_LOCATION, request.user.username, folder, filename)
        # await sync_to_async(zipfolder, thread_sensitive=True)
        shutil.make_archive(path, "zip", path)    
        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                    "movieListChanged": None,
                    "showMessage": "Zip File berhasil, tunggu beberapa saat apabila file zip belum ada"
                })
            })
    else:
        folder = request.GET.get("folder")
        filename = request.GET.get("filename")
        
    return render(request, 'filemanager/download_folder.html', {
        'folder': folder,
        'filename': filename,
    })

@csrf_exempt
def rename_file(request):
    if request.method == "POST":
        newname = request.POST.get('newname')
        folder = request.POST.get("folder")
        filename = request.POST.get("filename")
        existingfile = os.path.join(settings.FM_LOCATION, request.user.username, folder, filename)
        newfile = os.path.join(settings.FM_LOCATION, request.user.username, folder, newname)
        if exists(existingfile):
            os.rename(existingfile, newfile)
            message = f"perubahan nama {filename} Sukses."
        else:
            message = f"perubahan nama {filename} Gagal."
                    
        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                    "movieListChanged": None,
                    "showMessage": message
                })
            })
    else:
        folder = request.GET.get("folder")
        filename = request.GET.get("filename")
        form = RenameFileForm(initial={'newname':filename, 'folder': folder, 'filename': filename})
    return render(request, 'filemanager/rename_file.html', {
        'form': form,
    })

@csrf_exempt
def add_folder(request):
    if request.method == "POST":
        foldername = request.POST.get('foldername')
        folder = request.POST.get("folder")
        newfolder = os.path.join(settings.FM_LOCATION, request.user.username, folder, foldername)
        if not exists(newfolder):
            os.mkdir(newfolder)
            message = f"penambahan folder {foldername} Sukses."
        else:
            message = f"penambahan folder {foldername} Gagal."
                    
        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                    "movieListChanged": None,
                    "showMessage": message
                })
            })
    else:
        slug = request.GET.get("slug")
        year = str(request.GET.get("year"))
        folder = request.GET.get("folder")
        form = AddFolderForm(initial={'folder': folder})
    return render(request, 'filemanager/add_folder.html', {
        'form': form,
    })

@csrf_exempt
def download(request):
    if not request.user.is_authenticated:
        return redirect('login')
    folder = request.GET.get("folder")
    filename = request.GET.get("filename")
    path = os.path.join(settings.FM_LOCATION, request.user.username, folder, filename)
    if exists(path):
        mime_type, encoding = mimetypes.guess_type(path)
        with open(path, 'rb') as pdf:
            response = HttpResponse(pdf.read(), content_type=f'{mime_type}')
            response['Content-Disposition'] = f'inline;filename={filename}'
            return response
    raise Http404

@csrf_exempt
def upload_file(request):
    if request.method == "POST":
        if request.FILES:
            folder = request.POST.get("folder")
            uploads = request.FILES.getlist('uploadfiles')
            for upload in uploads:
                # pathlist = [__package__.split('.')[1], slug, year, str(folder).replace(os.path.sep, '$$'), str(upload)]
                # filetmpname = "$$".join(pathlist)
                # filetmppath = os.path.join(settings.MEDIA_ROOT, "tmpfiles", filetmpname)
                # fss = FileSystemStorage()
                # fss.save(filetmppath, upload)
                path = os.path.join(settings.FM_LOCATION, request.user.username, folder, str(upload))
                fss = FileSystemStorage()
                fss.save(path, upload)
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "movieListChanged": None,
                        "showMessage": 'Upload File Sukses, tunggu beberapa saat kemudian refresh halaman'
                    })
                })
    else:
        folder = request.GET.get("folder")
    return render(request, 'filemanager/upload_file.html', {
        'folder': folder
    })
