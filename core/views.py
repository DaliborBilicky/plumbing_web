from django.shortcuts import render


def homepage(request):
    return render(request, "core/home.html")


def services(request):
    return render(request, "core/services.html")
