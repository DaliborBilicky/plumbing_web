from django.contrib import admin

from .models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("name", "service_type", "email", "date", "time")
    search_fields = ("name", "email", "service_type")
    list_filter = ("service_type", "date")
