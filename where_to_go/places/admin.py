from django.contrib import admin
from .models import Place, Image


# Register your models here.
@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ['title', 'description_short', 'coordinate_lng', 'coordinate_lat']
    list_editable = ['description_short']


