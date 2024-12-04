import re
from datetime import datetime, time, timedelta

from django import forms
from django.utils.timezone import make_aware, now

from .models import Reservation


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = [
            "name",
            "service_type",
            "email",
            "phone",
            "date",
            "time",
            "special_requests",
        ]

    name = forms.CharField(
        label="Celé meno",
        max_length=120,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Zadajte celé meno"}
        ),
    )

    service_type = forms.ChoiceField(
        label="Druh opravy",
        choices=[
            ("", "Vyber druh opravy..."),
            ("waterPlumbing", "Voda"),
            ("gasPlumbing", "Plyn"),
            ("heatingPlumbing", "Kúrenie"),
            ("boilerPlumbing", "Kotol"),
        ],
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    email = forms.EmailField(
        label="Emailová adresa",
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Zadajte email"}
        ),
    )

    phone = forms.CharField(
        label="Telefóne číslo",
        max_length=15,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Zadajte telefóne číslo"}
        ),
    )

    date = forms.DateField(
        label="Dátum rezervácie",
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "type": "date",
                "min": now().date().isoformat(),
            }
        ),
    )

    time = forms.TimeField(
        label="Čas rezervácie",
        widget=forms.TimeInput(
            attrs={
                "class": "form-control",
                "type": "time",
                "min": "08:00",
                "max": "16:00",
            }
        ),
    )

    special_requests = forms.CharField(
        label="Doplnkové informácie",
        required=False,
        widget=forms.Textarea(
            attrs={"class": "form-control", "rows": 3, "placeholder": "Text píšte sem"}
        ),
    )

    def clean_time(self):
        input_time = self.cleaned_data.get("time")

        work_start = time(8, 0)
        work_end = time(16, 0)

        if input_time is None:
            raise forms.ValidationError("Prosím, zadajte platný čas.")

        if input_time < work_start or input_time > work_end:
            raise forms.ValidationError(
                "Čas musí byť v rámci pracovných hodín (8:00 - 16:00)."
            )

        return input_time

    def clean(self):
        cleaned_data = super().clean()
        input_date = cleaned_data.get("date")
        input_time = cleaned_data.get("time")

        if input_date and input_time:
            current_time = now()

            input_datetime = datetime.combine(input_date, input_time)

            input_datetime = make_aware(input_datetime, current_time.tzinfo)

            if input_date == current_time.date():
                if input_datetime <= current_time + timedelta(hours=5):
                    raise forms.ValidationError(
                        "Pre dnešné rezervácie musí byť čas aspoň 5 hodín od teraz."
                    )

        return cleaned_data
