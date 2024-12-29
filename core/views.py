import json

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import LoginForm, ProfileEditForm, ReservationForm, SignUpForm
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
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.save()
            return HttpResponseRedirect("/booking?posted=True")
    else:
        form = ReservationForm()
        if "posted" in request.GET:
            posted = True
    return render(request, "core/booking.html", {"form": form, "posted": posted})


def reservations(request):
    reservations_list = Reservation.objects.filter(user=request.user)
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

    return render(
        request,
        "core/edit_reservation.html",
        {"form": form, "reservation": reservation},
    )


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


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("homepage")
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = LoginForm()
    return render(request, "core/login.html", {"form": form})


def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("profile_edit")
    else:
        form = SignUpForm()

    return render(request, "core/signup.html", {"form": form})


def check_password_match(request):
    if request.method == "POST":
        data = json.loads(request.body)
        password = data.get("password")
        confirm_password = data.get("confirm_password")

        match = password == confirm_password

        return JsonResponse({"match": match})


@login_required
def profile_edit_view(request):
    user = request.user
    user_profile = user.profile

    if request.method == "POST":
        form = ProfileEditForm(request.POST, instance=user, user_profile=user_profile)
        if form.is_valid():
            form.save()
            return redirect("homepage")
    else:
        form = ProfileEditForm(instance=user, user_profile=user_profile)

    return render(request, "core/edit_profile.html", {"form": form})


def password_reset(request):
    if request.method == "POST":
        username = request.POST.get("username")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, "core/password_reset.html")

        try:
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            messages.success(request, "Password reset successfully!")
            return redirect("login")
        except User.DoesNotExist:
            messages.error(request, "User with this username does not exist!")

    return render(request, "core/password_reset.html")
