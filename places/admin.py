from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin, SortableTabularInline, SortableAdminBase
from django.utils.html import format_html
from .models import Place, Image


class PreviewMixin:
    @staticmethod
    def get_preview(obj):
        return format_html(
            '<img style="max-height:{height}" src="{url}"/>',
            height='200px',
            url=obj.image.url
        )


class ImageInline(SortableTabularInline, PreviewMixin):
    model = Image
    fields = ['position', 'image', 'get_preview']
    readonly_fields = ['get_preview']
    extra = 5


@admin.register(Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    inlines = [ImageInline]
    list_display = ['title', 'description_short', 'lng', 'lat']
    list_editable = ['description_short', 'lng', 'lat']


@admin.register(Image)
class ImageAdmin(SortableAdminMixin, admin.ModelAdmin, PreviewMixin):
    list_display = ['id', 'get_preview', 'place', 'position']
    readonly_fields = ['get_preview']
