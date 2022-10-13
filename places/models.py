from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from tinymce.models import HTMLField


class Place(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description_short = models.TextField()
    description_long = HTMLField()
    lng = models.DecimalField(
        max_digits=17,
        decimal_places=14,
        validators=[
            MinValueValidator(limit_value=-180),
            MaxValueValidator(limit_value=180)
        ]
    )
    lat = models.DecimalField(
        max_digits=16,
        decimal_places=14,
        validators=[
            MinValueValidator(limit_value=-90),
            MaxValueValidator(limit_value=90)
        ]
    )

    def __str__(self):
        return self.title


class Image(models.Model):
    image = models.ImageField(upload_to='place_images')
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='images')
    position = models.IntegerField(default=0)

    class Meta:
        ordering = ['position']

    def __str__(self):
        return f'{self.place.title}'
