from django.db import models

# Create your models here.
class UrlShort(models.Model):
    original_url = models.URLField()
    short_url = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

 