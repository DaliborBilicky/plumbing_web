from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Reservation(models.Model):
    SERVICE_CHOICES = [
        ("waterPlumbing", "Voda"),
        ("gasPlumbing", "Plyn"),
        ("heatingPlumbing", "Kúrenie"),
        ("boilerPlumbing", "Kotol"),
    ]

    name = models.CharField(max_length=100, verbose_name="Celé meno")
    service_type = models.CharField(
        max_length=20, choices=SERVICE_CHOICES, verbose_name="Druh opravy"
    )
    email = models.EmailField(verbose_name="Emailová adresa")
    phone = PhoneNumberField(max_length=15, verbose_name="Telefóne číslo")
    date = models.DateField(verbose_name="Dátum rezervácie")
    time = models.TimeField(verbose_name="Čas rezervácie")
    special_requests = models.TextField(blank=True, verbose_name="Doplnkové informácie")

    def __str__(self):
        return f"{self.name} - {self.service_type} ({self.date} at {self.time})"
