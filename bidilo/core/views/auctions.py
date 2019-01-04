from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import View

from core.forms import AuctionCreateForm
from core.models import Auction


def auctions(request):
    auction_list = Auction.objects.all()
    return render(request, 'core/auctions.html', {'auction_list': auction_list})


def description(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id)
    return render(request, 'core/auction.html', {'auction': auction})


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
