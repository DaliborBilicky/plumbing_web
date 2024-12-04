from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import ReservationForm


def homepage(request):
    return render(request, "core/home.html", {})


def services(request):
    return render(request, "core/services.html", {})


def booking(request):
    posted = False
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/booking?posted=True")
    else:
        form = ReservationForm()
        if "posted" in request.GET:
            posted = True
        return render(request, "core/booking.html", {"form": form, "posted": posted})


