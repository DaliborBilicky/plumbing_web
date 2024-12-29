from django.contrib.auth.models import User
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Reservation(models.Model):
    SERVICE_CHOICES = [
        ("waterPlumbing", "Voda"),
        ("gasPlumbing", "Plyn"),
        ("heatingPlumbing", "Kúrenie"),
        ("boilerPlumbing", "Kotol"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reservations",
        verbose_name="Používateľ",
    )

    service_type = models.CharField(
        max_length=20, choices=SERVICE_CHOICES, verbose_name="Druh opravy"
    )
    date = models.DateField(verbose_name="Dátum rezervácie")
    time = models.TimeField(verbose_name="Čas rezervácie")
    special_requests = models.TextField(blank=True, verbose_name="Doplnkové informácie")

    def __str__(self):
        return f"{self.user} - {self.service_type} ({self.date} at {self.time})"


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="Používateľ",
    )
    phone = PhoneNumberField(
        null=True, blank=True, max_length=15, verbose_name="Telefóne číslo"
    )

    def __str__(self):
        return f"{self.user}"
