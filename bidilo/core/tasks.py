from celery import shared_task
from django.conf import settings

from core.models import Auction


@shared_task
def finish_auction_time(auction_id):
    auction = Auction.objects.get(id=auction_id)
    auction.finish()
    finalize_auction.apply_async((auction_id,), countdown=settings.AUCTION_PAYBACK_TIME)


@shared_task
def finalize_auction(auction_id):
    auction = Auction.objects.get(id=auction_id)
    auction.finalize()
