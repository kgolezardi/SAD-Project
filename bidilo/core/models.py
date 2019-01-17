from django.conf import settings
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
    receive_date = models.DateTimeField(null=True, blank=True, verbose_name='Receipt date')

    @property
    def highest_bid(self):
        return self.bid_set.last()

    @property
    def finished(self):
        return self.deadline < timezone.now()

    def receive(self):
        highest_bid = self.highest_bid
        highest_bid.owner.pay(highest_bid.price)
        # FIXME: send notification
        self.owner.charge_credit(highest_bid.price)
        self.received = True
        self.receive_date = timezone.now()
        self.save()

    def save(self, *args, **kwargs):
        if not self.id:
            self.pub_date = timezone.now()
        return super().save(*args, **kwargs)

    def valid_price(self, price):
        return price < self.base_price + settings.MIN_INCREMENT_LIMIT or \
               self.highest_bid is not None and price < self.highest_bid.price + settings.MIN_INCREMENT_LIMIT

    def place_bid(self, user, price):
        # FIXME: atomic
        highest_bid = self.highest_bid
        if highest_bid is not None:
            highest_bid.owner.release_credit(highest_bid.price)
            # FIXME: send notification
        user.reserve_credit(price)
        bid = Bid(owner=user, auction=self, price=price)
        bid.save()


class Bid(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    date = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.date = timezone.now()
        return super().save(*args, **kwargs)
