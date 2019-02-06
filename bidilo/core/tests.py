import datetime
from django.test import TestCase
from django.utils import timezone

from accounts.models import User, Customer, Supervisor
from core.models import Auction, Report


class ModelTests(TestCase):
    def setUp(self):
        self.ali_user = User.objects.create_user(username='ali', email='ali@test.tst', password='alipass')
        self.mahdi_user = User.objects.create_user(username='mahdi', email='mahdi@test.tst', password='mahdipass')
        self.parsa_user = User.objects.create_user(username='parsa', email='parsa@test.tst', password='parsapass')
        self.kiarash_user = User.objects.create_user(username='kiarash', email='kiarash@test.tst',
                                                     password='kiarashpass')
        self.ali = Customer.objects.create(user=self.ali_user)
        self.mahdi = Customer.objects.create(user=self.mahdi_user)
        self.parsa = Customer.objects.create(user=self.parsa_user, credit=500)
        self.kiarash = Supervisor.objects.create(user=self.kiarash_user)
        self.ali_auction = Auction.objects.create(owner=self.ali, deadline=timezone.now() + datetime.timedelta(days=3),
                                                  base_price=100)
        self.mahdi_auction = Auction.objects.create(owner=self.mahdi,
                                                    deadline=timezone.now() - datetime.timedelta(days=3),
                                                    base_price=1000)

    def test_report_count_with_repeated_user(self):
        """
            report_count must not count repeated user 
        """
        Report.objects.create(reported_auction=self.ali_auction, reporter_customer=self.mahdi)
        Report.objects.create(reported_auction=self.ali_auction, reporter_customer=self.mahdi)
        Report.objects.create(reported_auction=self.ali_auction, reporter_customer=self.parsa)
        self.assertEqual(self.ali_auction.report_count, 2)

    def test_finished(self):
        self.assertEqual(self.ali_auction.finished, False)
        self.assertEqual(self.mahdi_auction.finished, True)

    def test_can_pay(self):
        self.assertEqual(self.parsa.can_pay(self.ali_auction.base_price), True)
        self.assertEqual(self.parsa.can_pay(self.mahdi_auction.base_price), False)

    def test_available_credit(self):
        self.assertEqual(self.parsa.available_credit, self.parsa.credit - self.parsa.reserved_credit)
