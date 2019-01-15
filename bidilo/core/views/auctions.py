from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import View

from core.forms import AuctionCreateForm
from core.models import Auction, Bid


def auctions(request):
    auction_list = Auction.objects.all()
    return render(request, 'core/auctions.html', {'auction_list': auction_list})


def description(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id)
    return render(request, 'core/auction.html', {'auction': auction})


@login_required
def offer_bid(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id)
    if auction.finilized:
        messages.add_message(request, messages.ERROR, 'The auction is now finished. You cannot offer bid for finished'
                                                      'aucitons.')
        return HttpResponseRedirect(reverse('core:description', args=(auction_id,)))
    highest_bid = auction.highest_bid
    price = int(request.POST.get("price", 0))
    if price < auction.base_price or highest_bid is not None and price < highest_bid.price:
        messages.add_message(request, messages.ERROR, 'Your price is not high enough. It should be higher than the '
                                                      'current highest bid and the base price.')
        return HttpResponseRedirect(reverse('core:description', args=(auction_id,)))
    bid = Bid(auction=auction, owner=request.user, price=price)
    bid.save()
    messages.add_message(request, messages.SUCCESS, 'You have successfully bid on this auction.')
    return HttpResponseRedirect(reverse('core:description', args=(auction_id,)))


class AuctionCreateView(View):
    template_name = "core/create_auction.html"

    def post(self, request):
        form = AuctionCreateForm(request.POST, owner=request.user)
        if form.is_valid():
            obj = form.save()
            return HttpResponseRedirect(reverse("core:description", kwargs={
                'auction_id': obj.id,
            }))

        return render(request, self.template_name, context={"form": form})

    def get(self, request):
        form = AuctionCreateForm(owner=request.user)
        return render(request, self.template_name, context={"form": form})
