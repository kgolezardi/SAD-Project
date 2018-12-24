from django import forms

from core.models import Auction


class AuctionCreateForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ['title', 'description', 'pub_date', 'base_price', 'deadline']
