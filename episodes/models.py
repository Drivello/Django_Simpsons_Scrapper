from django.db import models

# Create your models here.
class Episode(models.Model):
    date = models.DateField(auto_now=False, auto_now_add=False)
    number = models.PositiveIntegerField()
    season_number = models.PositiveIntegerField()   
    name = models.CharField(max_length=100)
    url = models.URLField(max_length=200)
    summary = models.TextField(blank=True)
    
    class Meta:
        ordering = ('date',)