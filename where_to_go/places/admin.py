from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin, SortableTabularInline
from django.utils.safestring import mark_safe
from .models import Place, Image


class ImageInline(SortableTabularInline):
    model = Image
    fields = ['position', 'image', 'get_preview']
    readonly_fields = ["get_preview"]
    extra = 5

    def get_preview(self, obj):
        width = 250
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.image.url,
            width=width,
            height=(width / obj.image.width)*obj.image.height,
            )
        )


@admin.register(Place)
class PlaceAdmin(SortableAdminMixin, admin.ModelAdmin):
    inlines = [ImageInline]
    list_display = ['id', 'title', 'description_short', 'coordinate_lng', 'coordinate_lat']
    ordering = ['id']
    list_editable = ['description_short', 'coordinate_lng', 'coordinate_lat']


@admin.register(Image)
class ImageAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ['id', 'get_preview', 'place', 'position']
    readonly_fields = ["get_preview"]

    def get_preview(self, obj):
        width = 300
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.image.url,
            width=width,
            height=(width / obj.image.width) * obj.image.height,
            )
        )
