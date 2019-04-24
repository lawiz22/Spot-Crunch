from django.contrib import admin

# Register your models here.
from .models import Album , Track, Artist

admin.site.register(Album)
admin.site.register(Track)
admin.site.register(Artist)