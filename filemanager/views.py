from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse

def index(request):
    return HttpResponse("tess")
