from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Place, Image


class ImageInline(admin.TabularInline):
    model = Image
    readonly_fields = ["get_preview"]
    ordering = ['position', 'id']
    extra = 3

    def get_preview(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.image.url,
            width=obj.image.width*0.3,
            height=obj.image.height*0.3,
            )
        )


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    inlines = [ImageInline]
    list_display = ['title', 'description_short', 'coordinate_lng', 'coordinate_lat']
    ordering = ['title']
    list_editable = ['description_short', 'coordinate_lng', 'coordinate_lat']


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_preview', 'place']
    readonly_fields = ["get_preview"]
    ordering = ['id']

    def get_preview(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.image.url,
            width=obj.image.width*0.22,
            height=obj.image.height*0.22,
            )
        )
