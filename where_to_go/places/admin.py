from django.contrib import admin
from .models import Place, Image


# Register your models here.

class ImageInline(admin.TabularInline):
    model = Image
    ordering = ['id']
    extra = 5


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    inlines = [ImageInline]
    list_display = ['title', 'description_short', 'coordinate_lng', 'coordinate_lat']
    list_editable = ['description_short']


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'image', 'place']
