from django.db import models
from tinymce.models import HTMLField


class Place(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description_short = models.TextField()
    description_long = HTMLField()
    coordinate_lng = models.DecimalField(max_digits=16, decimal_places=14)
    coordinate_lat = models.DecimalField(max_digits=16, decimal_places=14)

    def __str__(self):
        return self.title


class Image(models.Model):
    image = models.ImageField(upload_to='place_images', blank=True)
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='images')
    position = models.IntegerField(default=0)

    class Meta:
        ordering = ['position']

    def __str__(self):
        return f'{self.place.title}'
