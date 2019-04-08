from django.contrib import admin

# Register your models here.
from .models import Album , Track

admin.site.register(Album)
admin.site.register(Track)