from django.conf import settings
from django.db import models
from django.utils import timezone

from accounts.models import User
from notifications.models import Notification


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
    finalized = models.BooleanField(default=False)

    @property
    def highest_bid(self):
        if self.finalized and not self.received:
            return None
        return self.bid_set.last()

    @property
    def finished(self):
        return self.deadline < timezone.now()

    def finish(self):
        # FIXME: specify which auction
        Notification.objects.create(user=self.owner,
                                    content='Your auction is now finished. You can go to your '
                                            'auction page to see the contact information for the '
                                            'highest bidder. You have 10 days to send the item to '
                                            'him/her.')
        # FIXME: send notification to highest bidder

    def finalize(self):
        if self.finalized:
            return
        highest_bid = self.highest_bid
        if self.highest_bid is not None:
            # FIXME: specify which auction
            Notification.objects.create(user=self.owner,
                                        content='You didn\'t send the item to the highest bidder in the valid time '
                                                'window. Your auction is now finalized.')
            Notification.objects.create(user=highest_bid.owner,
                                        content='Unfortunately the auction owner didn\'t send the item in time. Your '
                                                'reserved money is now available for you to use it in other '
                                                'transactions.')
            highest_bid.owner.release_credit(highest_bid.price)
        self.finalized = True
        self.save()

    def receive(self):
        highest_bid = self.highest_bid
        highest_bid.owner.pay(highest_bid.price)
        # FIXME: specify which auction
        Notification.objects.create(user=self.owner,
                                    content='Your item has been received.')
        Notification.objects.create(user=highest_bid.owner,
                                    content='Congratulations on your new item!')
        self.owner.charge_credit(highest_bid.price)
        self.received = True
        self.finalized = True
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
        # TODO: atomic
        highest_bid = self.highest_bid
        if highest_bid is not None:
            highest_bid.owner.release_credit(highest_bid.price)
            # FIXME: specify which auction
            Notification.objects.create(user=self.owner,
                                        content='Someone just placed a higher bid on your item')
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
