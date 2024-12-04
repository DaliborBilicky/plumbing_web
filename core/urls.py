from django.urls import path

from . import views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("services", views.services, name="services"),
    path("booking", views.booking, name="booking"),
    path("reservations", views.reservations, name="reservations"),
]
