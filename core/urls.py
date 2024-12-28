from django.urls import path

from . import views
from .views import check_availability, login_view

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("services", views.services, name="services"),
    path("booking", views.booking, name="booking"),
    path("reservations", views.reservations, name="reservations"),
    path("edit/<int:reservation_id>/", views.edit_reservation, name="reservation_edit"),
    path(
        "delete/<int:reservation_id>/",
        views.delete_reservation,
        name="reservation_delete",
    ),
    path("check_availability/", check_availability, name="check_availability"),
    path("login/", login_view, name="login"),
]
