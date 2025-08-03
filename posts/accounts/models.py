# accounts/models.py
from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils import timezone
from datetime import timedelta

class PendingSignup(models.Model):
    """
    Temporary storage for users who have not yet verified their email.
    """
    email       = models.EmailField(unique=True)
    username    = models.CharField(max_length=150)
    password    = models.CharField(max_length=128)  # hashed later
    otp         = models.CharField(max_length=6)
    created_at  = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=10)
