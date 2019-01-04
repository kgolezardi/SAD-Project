from django.db import models
from django.utils import timezone

from accounts.models import User


class Auction(models.Model):
    title = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    short_description = models.TextField(max_length=500, help_text='Enter a brief description of your item to show'
                                                                   'in the auctions list')

    description = models.TextField(max_length=1000, help_text='Enter a more detailed description of your item')
    pub_date = models.DateTimeField(verbose_name='Publication date')
    base_price = models.PositiveIntegerField(default=10000, help_text='Base price in Tomans')
    deadline = models.DateTimeField(verbose_name='Finish date')

    def save(self, *args, **kwargs):
        if not self.id:
            self.pub_date = timezone.now()
        return super().save(*args, **kwargs)
