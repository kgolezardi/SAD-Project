from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import Auction

def auctions(request):
    auction_list = Auction.objects.all()
    return render(request, 'core/auctions.html', {'auction_list': auction_list})

def description(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id)
    return render(request, 'core/auction.html', {'auction': auction})
