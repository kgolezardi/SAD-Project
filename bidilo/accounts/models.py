from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # add additional fields in here
    credit = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.username
