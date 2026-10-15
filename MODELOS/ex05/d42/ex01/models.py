from django.db import models

# Create your models here.
class Movies(models.Model):
    title = models.CharField(max_length=64, unique=True, null=True)
    episode_nb = models.IntegerField(primary_key=True)
    opening_crawl = models.TextField(null=True, blank=True)
    director = models.CharField(max_length=32, null=True)
    producer = models.CharField(max_length=128, null=True)
    release_data = models.DateField(null=True)

    def __str__(self):
        return self.title