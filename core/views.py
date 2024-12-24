import json

from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ReservationForm
from .models import Reservation


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


def reservations(request):
    reservations_list = Reservation.objects.all()
    paginator = Paginator(reservations_list, 10)
    page = request.GET.get("page")
    reservations_page = paginator.get_page(page)

    return render(
        request,
        "core/reservations.html",
        {
            "reservations_list": reservations_list,
            "reservations_page": reservations_page,
        },
    )


def edit_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)

    if request.method == "POST":
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            return redirect("reservations")
    else:
        form = ReservationForm(instance=reservation)

    return render(request, "core/edit.html", {"form": form, "reservation": reservation})


def delete_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)

    if request.method == "POST":
        reservation.delete()
        return redirect("reservations")

    return render(request, "core/delete_confirm.html", {"reservation": reservation})


def check_availability(request):
    if request.method == "POST":
        data = json.loads(request.body)
        date = data.get("date")
        time = data.get("time")

        available = not Reservation.objects.filter(date=date, time=time).exists()

        return JsonResponse({"available": available})
