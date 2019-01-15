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
    received = models.BooleanField(default=False)
    receive_date = models.DateTimeField(null=True, verbose_name='Receipt date')

    @property
    def highest_bid(self):
        return self.bid_set.last()

    @property
    def finilized(self):
        return self.deadline < timezone.now()

    def receive(self):
        self.received = True
        self.receive_date = timezone.now()
        self.save()

    def save(self, *args, **kwargs):
        if not self.id:
            self.pub_date = timezone.now()
        return super().save(*args, **kwargs)


class Bid(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    date = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.date = timezone.now()
        return super().save(*args, **kwargs)
