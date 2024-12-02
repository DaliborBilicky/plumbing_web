from django.urls import path

from . import views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("services", views.services, name="services"),
]
