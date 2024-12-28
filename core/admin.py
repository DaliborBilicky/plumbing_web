from django.contrib import admin

from .models import Reservation, UserProfile

admin.site.register(Reservation)
admin.site.register(UserProfile)
