from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def start(request):
    template = 'places/index.html'
    return render(request, template)
