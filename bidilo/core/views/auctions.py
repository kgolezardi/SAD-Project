from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import View

from core.errors import AuctionFinishedError, PriceValidationError, UserAccessError, LowCreditError, \
    AuctionNotFinishedError, AuctionReceivedError, AuctionFinalizedError
from core.forms import AuctionCreateForm
from core.models import Auction
from core.tasks import finish_auction_time


def auctions(request):
    auction_list = Auction.objects.filter()
    return render(request, 'core/auctions.html', {'auction_list': auction_list})


def description(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id)
    return render(request, 'core/auction.html', {'auction': auction})


# FIXME: transactions
# TODO: unapproved auctions (transaction assignment)
# TODO: approve/unapprove auction
# TODO: my auctions (pending, ongoing, finished, finalized, rejected, suspended)
# TODO: edit/delete auction while pending
# TODO: reports
# TODO: suspend auction (see num. of reports)
# TODO: auction labels (yours, highest)


@login_required
@user_passes_test(lambda u: u.is_customer)
def offer_bid(request, auction_id):
    AUCTION_FINISHED_MESSAGE = 'The auction is now finished. You cannot offer bid for finished aucitons.'
    LOW_PRICE_MESSAGE = 'Your price is not high enough. It should be higher than the base price the current highest ' \
                        'bid plus the minimum bid increment (%s).' % settings.MIN_INCREMENT_LIMIT
    OWN_AUCTION_MESSAGE = 'You cannot bid on your own auction.'
    SUCCESSFULL_BID_MESSAGE = 'You have successfully bid on this auction.'
    NO_CREDIT_MESSAGE = 'You do not have enough credit in your account. Please charge your credit before offering a ' \
                        'higher bid.'

    auction = get_object_or_404(Auction, id=auction_id)
    price = int(request.POST.get("price", 0))
    customer = request.user.customer

    try:
        auction.place_bid(customer, price)
        messages.success(request, SUCCESSFULL_BID_MESSAGE)
    except AuctionFinishedError:
        messages.error(request, AUCTION_FINISHED_MESSAGE)
    except PriceValidationError:
        messages.error(request, LOW_PRICE_MESSAGE)
    except UserAccessError:
        messages.error(request, OWN_AUCTION_MESSAGE)
    except LowCreditError:
        messages.error(request, NO_CREDIT_MESSAGE)

    return HttpResponseRedirect(reverse('core:description', args=(auction_id,)))


@login_required
@user_passes_test(lambda u: u.is_customer)
def confirm_receipt(request, auction_id):
    FINALIZED_MESSAGE = 'The auction is finalized'
    INVALID_USER_MESSAGE = 'You are not the highest bidder.'
    UNFINISHED_MESSAGE = 'The auciton is not finished yet.'
    ALREADY_RECEIVED_MESSAGE = 'The item is already received.'
    SUCCESSFULL_RECEIVE_MESSAGE = 'You have successfully received the item.'

    auction = get_object_or_404(Auction, id=auction_id)
    customer = request.user.customer

    try:
        auction.receive(customer)
        messages.success(request, SUCCESSFULL_RECEIVE_MESSAGE)
    except AuctionNotFinishedError:
        messages.error(request, UNFINISHED_MESSAGE)
    except UserAccessError:
        messages.error(request, INVALID_USER_MESSAGE)
    except AuctionReceivedError:
        messages.error(request, ALREADY_RECEIVED_MESSAGE)
    except AuctionFinalizedError:
        messages.error(request, FINALIZED_MESSAGE)

    return HttpResponseRedirect(reverse('core:description', args=(auction_id,)))


class AuctionCreateView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = "core/create_auction.html"

    def test_func(self):
        return self.request.user.is_customer

    def post(self, request):
        form = AuctionCreateForm(request.POST, request.FILES, owner=request.user.customer)
        if form.is_valid():
            obj = form.save()
            finish_auction_time.apply_async((obj.id,), eta=obj.deadline)
            return HttpResponseRedirect(reverse("core:description", kwargs={
                'auction_id': obj.id,
            }))

        return render(request, self.template_name, context={"form": form})

    def get(self, request):
        form = AuctionCreateForm(owner=request.user.customer)
        return render(request, self.template_name, context={"form": form})
