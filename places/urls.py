from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import start, get_details_url

urlpatterns = [
    path('', start, name='start'),
    path('places/<int:pk>', get_details_url, name='details_url')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
