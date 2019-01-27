from django.db import models
from django.utils import timezone

from accounts.models import User


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(verbose_name='Publication date')
    content = models.TextField(max_length=1000)
    read = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.date = timezone.now()
        return super().save(*args, **kwargs)

    def set_read(self):
        self.read = True
        self.save()

    def set_unread(self):
        self.read = False
        self.save()
