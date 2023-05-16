from django.contrib import admin
from .models import Episode

# Register your models here.

class EpisodeAdmin(admin.ModelAdmin):
    list_display = ['date', 'number', 'season_number', 'name', 'url', 'summary']

admin.site.register(Episode, EpisodeAdmin)