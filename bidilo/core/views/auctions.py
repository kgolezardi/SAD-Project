from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404
from django.http import HttpResponseForbidden
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views import generic

from core.errors import AuctionFinishedError, PriceValidationError, UserAccessError, LowCreditError, \
    AuctionNotFinishedError, AuctionReceivedError, AuctionFinalizedError, AuctionStateError
from core.forms import AuctionCreateForm, AuctionChangeForm
from core.models import Auction, Bid, AuctionImage, Report
from core.tasks import finish_auction_time


def auctions(request):
    auction_list = Auction.objects.filter(state=Auction.APPROVED)
    return render(request, 'core/auctions.html', {'auction_list': auction_list})


def description(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id)
    user = request.user
    if auction.state != Auction.APPROVED:
        if not user.is_authenticated or user.is_customer and auction.owner.user != user:
            raise Http404
    return render(request, 'core/auction.html', {'auction': auction})


@login_required
@user_passes_test(lambda u: u.is_supervisor)
def pending_auctions_view(request):
    auction_list = Auction.objects.filter(state=Auction.PENDING)
    return render(request, 'core/auctions.html', {'auction_list': auction_list,
                                                  'pending': True})


@login_required
@user_passes_test(lambda u: u.is_supervisor)
def approve_auction(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id)
    supposed_update = request.POST.get('last_update')
    actual_update = auction.last_update
    if supposed_update == actual_update.isoformat():
        if auction.state == Auction.PENDING:
            finish_auction_time.apply_async((auction.id,), eta=auction.deadline)
            auction.approve()
    else:
        messages.error(request, "The auction info had been changed since you last visit.")

    return HttpResponseRedirect(reverse('core:description', args=(auction_id,)))


@login_required
@user_passes_test(lambda u: u.is_supervisor)
def reject_auction(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id)
    supposed_update = request.POST.get('last_update')
    actual_update = auction.last_update
    if supposed_update == actual_update.isoformat():
        if auction.state == Auction.PENDING:
            auction.reject()
    else:
        messages.error(request, "The auction info had been changed since you last visit.")

    return HttpResponseRedirect(reverse('core:description', args=(auction_id,)))

@login_required
@user_passes_test(lambda u: u.is_supervisor)
def suspend_auction(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id)
    if auction.state == Auction.APPROVED:
        auction.suspend()
    return HttpResponseRedirect(reverse('core:description', args=(auction_id,)))


# FIXME: transactions
# DONE: unapproved auctions (transaction assignment)
# DONE: approve/unapprove auction
# DONE: my auctions (pending, ongoing, finished, rejected, suspended) / purchases
# DONE: edit/delete auction while pending
# TODO: reports
# TODO: suspend auction (see num. of reports)
# TODO: auction labels (yours, highest)


@login_required
@user_passes_test(lambda u: u.is_customer)
def my_actions(request):
    customer = request.user.customer
    pending_auctions = Auction.objects.filter(owner=customer, state=Auction.PENDING)
    approved_auctions = list(Auction.objects.filter(owner=customer, state=Auction.APPROVED))
    ongoing_auctions = [auction for auction in approved_auctions if not auction.finished]
    finished_auctions = [auction for auction in approved_auctions if auction.finished]
    rejected_auctions = Auction.objects.filter(owner=customer, state=Auction.REJECTED)
    return render(request, 'core/my_auctions.html', {'pending_auctions': pending_auctions,
                                                     'ongoing_auctions': ongoing_auctions,
                                                     'finished_auctions': finished_auctions,
                                                     'rejected_auctions': rejected_auctions})


@login_required
@user_passes_test(lambda u: u.is_customer)
def my_purchases(request):
    customer = request.user.customer
    my_bids = Bid.objects.filter(owner=customer)
    purchases = [bid.auction for bid in my_bids if bid.auction.highest_bid == bid]
    return render(request, 'core/my_purchases.html', {'auction_list': purchases})


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
    except AuctionStateError:
        raise Http404
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
    except AuctionStateError:
        raise Http404
    except AuctionNotFinishedError:
        messages.error(request, UNFINISHED_MESSAGE)
    except UserAccessError:
        messages.error(request, INVALID_USER_MESSAGE)
    except AuctionReceivedError:
        messages.error(request, ALREADY_RECEIVED_MESSAGE)
    except AuctionFinalizedError:
        messages.error(request, FINALIZED_MESSAGE)

    return HttpResponseRedirect(reverse('core:description', args=(auction_id,)))


@login_required
@user_passes_test(lambda u: u.is_customer)
def remove_auction(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id)
    if auction.owner == request.user.customer and auction.state == Auction.PENDING:
        auction.delete()
        return HttpResponseRedirect(reverse('core:auctions'))
    messages.error(request, "You don't have access to remove this auction right now.")
    return HttpResponseRedirect(reverse('core:description', args=(auction_id,)))


@login_required
@user_passes_test(lambda u: u.is_customer)
def report_auction(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id)
    reason = str(request.POST.get('reason', ''))
    if auction.owner != request.user.customer and auction.state == Auction.APPROVED:
        Report.objects.create(reporter_customer=request.user.customer, reported_auction=auction, reason=reason)
    return HttpResponseRedirect(reverse('core:description', args=(auction_id,)))


@login_required
@user_passes_test(lambda u: u.is_customer)
def delete_image(request, auction_id, image_id):
    auction = get_object_or_404(Auction, id=auction_id)
    image = get_object_or_404(AuctionImage, id=image_id)
    if auction.owner == request.user.customer and auction.state == Auction.PENDING and \
            image.auction == auction:
        image.delete()
        return HttpResponseRedirect(reverse('core:edit_auction', args=(auction_id,)))
    messages.error(request, "You don't have access to remove this image right now.")
    return HttpResponseRedirect(reverse('core:edit_auciton', args=(auction_id,)))


class AuctionEditView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Auction
    form_class = AuctionChangeForm
    template_name = 'core/edit_auction.html'

    def test_func(self):
        return self.request.user.is_customer

    def get_object(self, queryset=None):
        auction_id = self.kwargs.get('auction_id')
        auction = get_object_or_404(Auction, id=auction_id)
        if auction.state != Auction.PENDING:
            raise Http404
        return auction

    def get_success_url(self):
        return reverse('core:description', args=(self.object.id,))

    def get_context_data(self, **kwargs):
        small_images = AuctionImage.objects.filter(auction=self.object)
        kwargs['small_images'] = small_images
        kwargs['auction_id'] = self.object.id
        return super().get_context_data(**kwargs)


class AuctionCreateView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = "core/create_auction.html"

    def test_func(self):
        return self.request.user.is_customer

    def post(self, request):
        form = AuctionCreateForm(request.POST, request.FILES, owner=request.user.customer)
        if form.is_valid():
            obj = form.save()
            return HttpResponseRedirect(reverse("core:description", kwargs={
                'auction_id': obj.id,
            }))

        return render(request, self.template_name, context={"form": form})

    def get(self, request):
        form = AuctionCreateForm(owner=request.user.customer)
        return render(request, self.template_name, context={"form": form})
