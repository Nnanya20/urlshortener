from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
import string
import random

from .models import UrlShort 


# Create your views here.
def generate_shorl_url():
    characters = string.ascii_letters + string.digits
    short = ''
    for i in range(6):
        short += random.choice(characters)
    return short

def index(request):
    if request.method =='POST':
        original_url = request.POST['original_url']
        short_url = generate_shorl_url()
        url, created = UrlShort.objects.get_or_create(original_url=original_url, short_url=short_url)
        return render(request, 'index.html', {'short_url':request.build_absolute_uri('/') + url.short_url})
    return render(request, 'index.html')

def redirect_url(request, short_url):
    url = get_object_or_404(UrlShort, short_url=short_url)
    return redirect(url.original_url)