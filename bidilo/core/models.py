import os
from uuid import uuid4

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from django.db import models
from django.utils import timezone

from accounts.models import User, Customer
from core.errors import AuctionFinishedError, PriceValidationError, UserAccessError, LowCreditError, \
    AuctionNotFinishedError, AuctionReceivedError, AuctionFinalizedError, AuctionStateError
from notifications.models import Notification


def auction_picture_validator(image):
    if image.size > settings.AUCTION_IMAGE_LIMIT_MB * 1024 * 1024:
        raise ValidationError("Images have size limit of %d megabytes" % settings.AUCTION_IMAGE_LIMIT_MB)
    width, height = get_image_dimensions(image)
    ratio = width / height
    if ratio < 1 or ratio > 1.75:
        raise ValidationError("Ratio of the images should be between 1 and 1.75")


def get_image_filename(instance, filename):
    return os.path.join('auction_images', '%s.jpg' % uuid4().hex)


class Auction(models.Model):
    PENDING = 0
    APPROVED = 1
    REJECTED = 2
    SUSPENDED = 3
    STATE_CHOICES = (
        (PENDING, 'pending'),
        (APPROVED, 'approved'),
        (REJECTED, 'rejected'),
        (SUSPENDED, 'suspended'),
    )

    title = models.CharField(max_length=50)
    owner = models.ForeignKey(Customer, on_delete=models.CASCADE)
    short_description = models.TextField(max_length=500, help_text='Enter a brief description of the item to show'
                                                                   'in the auctions list')
    description = models.TextField(max_length=1000, help_text='Enter a more detailed description of the item')
    pub_date = models.DateTimeField(verbose_name='Publication date')
    last_update = models.DateTimeField()
    picture = models.ImageField(upload_to=get_image_filename, validators=[auction_picture_validator],
                                help_text='The main image for the auction')
    base_price = models.PositiveIntegerField(default=10000, help_text='Base price in Tomans')
    deadline = models.DateTimeField(verbose_name='Finish date')
    received = models.BooleanField(default=False)
    receive_date = models.DateTimeField(null=True, blank=True, verbose_name='Receipt date')
    finalized = models.BooleanField(default=False)
    state = models.IntegerField(choices=STATE_CHOICES, default=PENDING)

    def save(self, *args, **kwargs):
        if not self.id:
            self.pub_date = timezone.now()
        self.last_update = timezone.now()
        return super().save(*args, **kwargs)

    @property
    def highest_bid(self):
        if self.finalized and not self.received:
            return None
        return self.bid_set.last()

    @property
    def finished(self):
        return self.deadline < timezone.now()

    @property
    def report_count(self):
        return self.report_set.order_by('reporter_customer_id').values('reporter_customer_id').distinct().count()

    def valid_price(self, price):
        return price < self.base_price or \
               self.highest_bid is not None and price < self.highest_bid.price + settings.MIN_INCREMENT_LIMIT

    def finish(self):
        if self.state != Auction.APPROVED:
            return
        Notification.objects.create(user=self.owner.user,
                                    content="Your auction '%s' is now finished. You can go to its page to see the "
                                            "contact information for the highest bidder. You have %d days to send the "
                                            "item to him/her." % (self.title, settings.AUCTION_PAYBACK_TIME.days))
        highest_bid = self.highest_bid
        if highest_bid is not None:
            Notification.objects.create(user=highest_bid.owner.user,
                                        content="The auction '%s' in which you have the highest bid is now finished. "
                                                "The owner is supposed to give you the item in %d days from now."
                                                % (self.title, settings.AUCTION_PAYBACK_TIME.days))

    def timeover_finalize(self):
        if self.finalized:
            return
        highest_bid = self.highest_bid
        if self.state == Auction.APPROVED and self.highest_bid is not None:
            Notification.objects.create(user=self.owner.user,
                                        content="You didn't send the item '%s' to the highest bidder in time window "
                                                "you were supposed to. Your auction is now finalized." % self.title)
            Notification.objects.create(user=highest_bid.owner.user,
                                        content="Unfortunately the owner of the auction '%s' didn't send the item in "
                                                "time. Your reserved money is now available for you to use it in other "
                                                "transactions." % self.title)
            highest_bid.owner.release_credit(highest_bid.price)
        self.finalized = True
        self.save()

    def place_bid(self, customer, price):
        if self.state != Auction.APPROVED:
            raise AuctionStateError()
        if self.finished:
            raise AuctionFinishedError()
        if self.valid_price(price):
            raise PriceValidationError()
        if customer == self.owner:
            raise UserAccessError()
        if not customer.can_pay(price):
            raise LowCreditError()

        highest_bid = self.highest_bid
        if highest_bid is not None:
            Notification.objects.create(user=highest_bid.owner.user,
                                        content="Someone just placed a higher bid than yours for item '%s'"
                                                % self.title)
            highest_bid.owner.release_credit(highest_bid.price)
        Notification.objects.create(user=self.owner.user,
                                    content="Someone just placed a bid on your item '%s'" % self.title)
        customer.reserve_credit(price)
        Bid.objects.create(owner=customer, auction=self, price=price)

    def receive(self, customer):
        highest_bid = self.highest_bid

        if self.state != Auction.APPROVED:
            raise AuctionStateError()
        if not self.finished:
            raise AuctionNotFinishedError()
        if highest_bid is None or highest_bid.owner != customer:
            raise UserAccessError()
        if self.received:
            raise AuctionReceivedError()
        if self.finalized:
            raise AuctionFinalizedError()

        highest_bid.owner.pay(highest_bid.price)
        Notification.objects.create(user=self.owner.user,
                                    content="Your item '%s' has been received by the new owner." % self.title)
        Notification.objects.create(user=highest_bid.owner.user,
                                    content="Congratulations on your new item '%s'!" % self.title)
        self.owner.charge_credit(highest_bid.price)
        self.received = True
        self.finalized = True
        self.receive_date = timezone.now()
        self.save()

    def approve(self):
        Notification.objects.create(user=self.owner.user,
                                    content="Your auction '%s' has been approved by our supervisors." % self.title)
        self.state = Auction.APPROVED
        self.save()

    def reject(self):
        Notification.objects.create(user=self.owner.user,
                                    content="Your auction '%s' has been rejected by our supervisors." % self.title)
        self.state = Auction.REJECTED
        self.save()

    def suspend(self):
        Notification.objects.create(user=self.owner.user,
                                    content="Your auction '%s' has been suspended by supervisors." % self.title)
        self.state = Auction.SUSPENDED
        self.save()
        if self.highest_bid is not None:
            Notification.objects.create(user=self.highest_bid.owner.user,
                                        content="Unfortunately the auction for which you had bid '%s' has been suspended."
                                                % self.title)
            self.highest_bid.owner.release_credit(self.highest_bid.price)
            self.bid_set.all().delete()





class AuctionImage(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    file = models.ImageField(upload_to=get_image_filename, validators=[auction_picture_validator])


class Bid(models.Model):
    owner = models.ForeignKey(Customer, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    date = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.date = timezone.now()
        return super().save(*args, **kwargs)


class Report(models.Model):
    reporter_customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    reported_auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    reason = models.TextField(max_length=200, help_text='Please specify the reason.')
    date = models.DateTimeField()
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
