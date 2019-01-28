from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    name = models.CharField(max_length=50, verbose_name="Display Name")
    phone_number = models.CharField(max_length=12)
    address = models.TextField(max_length=500, help_text='Address for other users to send you the items you buy.')
    credit = models.PositiveIntegerField(default=0)
    reserved_credit = models.PositiveIntegerField(default=0)

    def can_pay(self, price):
        return price <= self.credit - self.reserved_credit

    def reserve_credit(self, price):
        self.reserved_credit += price
        self.save()

    def release_credit(self, price):
        self.reserved_credit -= price
        self.save()

    def charge_credit(self, price):
        self.credit += price
        self.save()

    def pay(self, price, from_reserved=True):
        if from_reserved:
            self.reserved_credit -= price
        self.credit -= price
        self.save()

    @property
    def available_credit(self):
        return self.credit - self.reserved_credit

    def __str__(self):
        return self.username
