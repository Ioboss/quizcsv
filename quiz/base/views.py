from django.shortcuts import render


def home(request):
    return render(request, 'base/home.html')


def perguntas(request):
    return render(request, 'base/game.html')


def podio(request):
    return render(request, 'base/podio.html')