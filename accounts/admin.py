from django.contrib import admin

# Register your models here.
from .models import PendingSignup

admin.site.register(PendingSignup)
