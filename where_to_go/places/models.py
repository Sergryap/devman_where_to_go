from django.db import models

# Create your models here.


class Place(models.Model):
    title = models.CharField(max_length=100)
    description_short = models.CharField(max_length=300)
    description_long = models.TextField()
    coordinate_lng = models.CharField(max_length=50)
    coordinate_lat = models.CharField(max_length=50)
    place_id = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.title


class Image(models.Model):
    image = models.ImageField(upload_to='place_images', blank=True)
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='images')
