from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render


def index(request):  # HttpRequest
    return HttpResponse("Страница приложения women.")


def categories(request, catid):
    if request.POST:
        print(request.POST)
    return HttpResponse("<h1>Статьи по категориям</h1><p>{catid}</p>")


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
