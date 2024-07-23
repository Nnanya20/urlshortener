from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.http import JsonResponse
import string
import random
from .models import UrlShort


# Function to generate a unique short URL
def generate_short_url():
    characters = string.ascii_letters + string.digits
    while True:
        short = ''.join(random.choices(characters, k=6))
        if not UrlShort.objects.filter(short_url=short).exists():
            return short


def index(request):
    error_message = None
    if request.method == 'POST':
        original_url = request.POST.get('original_url', '').strip()

        # Validate the URL
        validator = URLValidator()
        try:
            validator(original_url)
        except ValidationError:
            error_message = "Invalid URL"
            return render(request, 'index.html', {'error': error_message})

        # Check if the URL is empty
        if not original_url:
            error_message = "URL cannot be empty"
            return render(request, 'index.html', {'error': error_message})

        # Check if the URL already has a short URL
        url = UrlShort.objects.filter(original_url=original_url).first()

        if url is None:
            short_url = generate_short_url()
            url = UrlShort.objects.create(original_url=original_url, short_url=short_url)

        return render(request, 'index.html', {'short_url': request.build_absolute_uri('/') + url.short_url})

    return render(request, 'index.html')


def redirect_url(request, short_url):
    url = get_object_or_404(UrlShort, short_url=short_url)
    return redirect(url.original_url)
