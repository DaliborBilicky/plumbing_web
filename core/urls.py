from django.urls import path

from . import views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("services", views.services, name="services"),
    path("booking", views.booking, name="booking"),
    path("reservations", views.reservations, name="reservations"),
    path(
        "reservation/edit/<int:reservation_id>/",
        views.edit_reservation,
        name="reservation_edit",
    ),
    path(
        "reservation/delete/<int:reservation_id>/",
        views.delete_reservation,
        name="reservation_delete",
    ),
    path("check_availability/", views.check_availability, name="check_availability"),
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path(
        "check_password_match/", views.check_password_match, name="check_password_match"
    ),
    path("profile/edit/", views.profile_edit_view, name="profile_edit"),
    path("password_reset/", views.password_reset, name="password_reset"),
]
