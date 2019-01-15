from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    name = models.CharField(max_length=50, verbose_name="Display Name")
    phone_number = models.CharField(max_length=12)
    address = models.TextField(max_length=500, help_text='Address for other users to send you the items you buy.')
    credit = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.username
