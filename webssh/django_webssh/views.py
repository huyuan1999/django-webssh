from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django_webssh.tools import tools
import json



def index(request):
    return render(request, 'index.html')
