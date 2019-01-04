from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # add additional fields in here
    credit = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.username
