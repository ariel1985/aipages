"""
from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    # return HttpResponse("Hello, world. You're at the start...")
    return render(request, 'index.html')
"""

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Pages
from django.core.serializers import serialize
import json

def index(request):
    pages = Pages.objects.all()
    return render(request, 'pages.html', { "pages": pages })
    # return render(request, 'index.html')

def add_page(request):
    return render(request, 'index.html')

def save_page(request):
    if(request.method=='POST'):
        html = request.POST['html']
        css = request.POST['css']
        page = Pages.objects.create(name="untitled", html=html, css=css)
        page.save()
    return JsonResponse({ "result" : (json.loads(serialize('json', [page])))[0]}) 
    # return JsonResponse({ "result" : {"html": html, "css": css }})

def edit_page(request, id):
    page = Pages.objects.get(pk=id)
    return render(request, 'index.html', {"page": page})

def edit_page_content(request, id):
    if(request.method=='POST'):
        html = request.POST['html']
        css = request.POST['css']
        page = Pages.objects.get(pk=id)
        page.html = html
        page.css = css
        page.save()
    return JsonResponse({ "result" : (json.loads(serialize('json', [page])))[0]})    

def preview_page(request, id):
    page = Pages.objects.get(pk=id)
    return render(request, 'preview.html', {"page": page})


def list_pages(request):
    pages = Pages.objects.all()
    return render(request, 'portfolio.html', { "pages": pages })