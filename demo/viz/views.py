from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    return HttpResponse("<p>Hola</p>")

def table_view(request, title):
    HttpResponse(f"<p> House: {title}")