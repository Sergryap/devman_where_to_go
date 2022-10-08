from django.db import models
from tinymce.models import HTMLField


class Place(models.Model):
    title = models.CharField(max_length=100)
    description_short = models.CharField(max_length=500)
    description_long = HTMLField()
    coordinate_lng = models.CharField(max_length=50)
    coordinate_lat = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Image(models.Model):
    image = models.ImageField(upload_to='place_images', blank=True)
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='images')
    position = models.IntegerField(default=0)

    class Meta:
        ordering = ['position']

    def __str__(self):
        return f"{self.place.title}"
