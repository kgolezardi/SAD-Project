from django import forms

from core.models import Auction


class AuctionCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.owner = kwargs.pop("owner")
        super().__init__(*args, **kwargs)

    class Meta:
        model = Auction
        fields = ['title', 'short_description', 'description', 'base_price', 'deadline']

    def save(self, commit=True):
        auction = super().save(commit=False)
        auction.owner = self.owner
        if commit:
            auction.save()
        return auction
