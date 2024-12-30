from datetime import datetime, time, timedelta

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.timezone import make_aware, now
from phonenumber_field.formfields import PhoneNumberField

from .models import Reservation


class LoginForm(forms.Form):
    username = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Pouzivatelske meno"}
        ),
    )

    password = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Heslo"}
        ),
    )


class ProfileEditForm(forms.ModelForm):
    username = forms.CharField(
        label="Pouzivatelske meno",
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Zadajte pouzivatelske meno"}
        ),
    )
    first_name = forms.CharField(
        label="Meno",
        max_length=30,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Zadajte meno"}
        ),
    )
    last_name = forms.CharField(
        label="Priezvisko",
        max_length=30,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Zadajte priezvisko"}
        ),
    )
    email = forms.EmailField(
        label="Emailová adresa",
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Zadajte email"}
        ),
    )
    phone = PhoneNumberField(
        label="Telefóne číslo",
        max_length=15,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Zadajte telefóne číslo"}
        ),
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]

    def __init__(self, *args, **kwargs):
        self.user_profile = kwargs.pop("user_profile", None)
        super().__init__(*args, **kwargs)
        if self.user_profile:
            self.fields["phone"].initial = self.user_profile.phone

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        if self.user_profile:
            self.user_profile.phone = self.cleaned_data.get("phone")
            self.user_profile.save()
        return user


class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password"]

    username = forms.CharField(
        label="Pouzivatelske meno",
        max_length=120,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Zadajte pouzivatelske meno"}
        ),
    )
    first_name = forms.CharField(
        label="Meno",
        max_length=30,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Zadajte meno"}
        ),
    )
    last_name = forms.CharField(
        label="Priezvisko",
        max_length=30,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Zadajte priezvisko"}
        ),
    )
    email = forms.EmailField(
        label="Emailová adresa",
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Zadajte email"}
        ),
    )
    password = forms.CharField(
        label="Heslo",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Zadajte heslo"}
        ),
    )
    password_confirmation = forms.CharField(
        label="Potvrdit heslo",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Potvrdit heslo"}
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")

        if password and password_confirmation and password != password_confirmation:
            self.add_error(None, "Hesla niesu rovnake")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = [
            "service_type",
            "date",
            "time",
            "special_requests",
        ]

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
                    self.add_error(
                        None,
                        "Pre dnešné rezervácie musí byť čas aspoň 5 hodín od teraz.",
                    )

            two_hour_range_start = input_datetime - timedelta(hours=2)
            two_hour_range_end = input_datetime + timedelta(hours=2)

            overlapping_reservations = Reservation.objects.filter(
                date=input_date,
                time__range=(two_hour_range_start.time(), two_hour_range_end.time()),
            )
            if overlapping_reservations.exists():
                self.add_error(
                    None,
                    "Tento termín je už rezervovaný. Vyberte iný dátum alebo čas. (aspoň 2 hodiny od existujúcej rezervácie)",
                )

        return cleaned_data
