from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class Profile(models.Model):
    ACCOUNT_USER_TYPE = [
        ("doctor","Doctor"),
        ("patient", "Patient"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    profile_image = models.ImageField(null=True, blank=True, default="user-default.png")
    account_user_type = models.CharField(max_length=10, choices=ACCOUNT_USER_TYPE)
    address = models.CharField(max_length=200, blank=True, null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return str(self.user.username)

import users.signals