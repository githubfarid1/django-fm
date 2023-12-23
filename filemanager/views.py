from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.views.decorators.csrf import csrf_exempt
import os
from django.conf import settings
from datetime import date, datetime
import mimetypes

def index(request):
    return HttpResponse("tess")

def build_breadcrumbs(url):
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
    result[-1]['link'] = ''
    return result

@csrf_exempt
def show_folder(request, slug, year):
    if not request.user.is_authenticated:
        return redirect('login')
    
    username = request.user.username
    folder = request.GET.get("folder")
    # dep = Department.objects.get(slug=slug)
    context = {
        'slug': slug,
        'year': year,
        # 'depname':dep.name,
        'depslug': slug,
        'breadcrumbs': build_breadcrumbs(folder),
        'folder': folder,
        'satkername': 'PJPA',
        'depurl': 'fm_pjpa_department',
        'deplisturl': 'fm_pjpa_department_list',
        'folderlisturl': 'fm_pjpa_folder_list',
        'downloadurl': 'fm_pjpa_download',
        'depyearurl': 'fm_pjpa_department_year',
        'showfolderurl': 'fm_pjpa_show_folder',
        'addfolderurl': 'fm_pjpa_add_folder',
        'uploadfileurl': 'fm_pjpa_upload_file'
    }
    return render(request=request, template_name='filemanager/show_folder.html', context=context)

@csrf_exempt
def folder_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    slug = request.GET.get("slug")
    year = request.GET.get("year")
    folder = request.GET.get("folder")
    
    folderlist = str(folder).split("/")
    folderlist.pop(0)
    path = os.path.join(settings.FM_LOCATION, __package__.split('.')[1], slug, year, folder)
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
    
    dep = Department.objects.get(slug=slug)        
    context = {
        'data': data,
        'folder': folder,
        'showfolderurl': 'fm_pjpa_show_folder',
        'downloadurl': 'fm_pjpa_download',
        'slug': slug,
        'year': year,
        'zipfolderurl':'fm_pjpa_download_folder',
        'renameurl': 'fm_pjpa_rename_file',
        'removeurl': 'fm_pjpa_remove_file',
        
}
    # return HttpResponse(context)
    return render(request=request, template_name='file_manager/folder_list.html', context=context)

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
