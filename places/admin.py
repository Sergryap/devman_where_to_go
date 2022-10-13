from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin, SortableTabularInline
from django.utils.html import format_html
from .models import Place, Image


class ImageInline(SortableTabularInline):
    model = Image
    fields = ['position', 'image', 'get_preview']
    readonly_fields = ['get_preview']
    extra = 5

    def get_preview(self, obj):
        return format_html(f'<img style="max-height:200px" src="{obj.image.url}"/>')


@admin.register(Place)
class PlaceAdmin(SortableAdminMixin, admin.ModelAdmin):
    inlines = [ImageInline]
    list_display = ['id', 'title', 'description_short', 'coordinate_lng', 'coordinate_lat']
    ordering = ['id']
    list_editable = ['description_short', 'coordinate_lng', 'coordinate_lat']


@admin.register(Image)
class ImageAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ['id', 'get_preview', 'place', 'position']
    readonly_fields = ['get_preview']

    def get_preview(self, obj):
        return format_html(f'<img style="max-height:200px" src="{obj.image.url}"/>')
