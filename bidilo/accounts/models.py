from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # add additional fields in here

    def __str__(self):
        return self.username
