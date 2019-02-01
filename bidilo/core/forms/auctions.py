from django import forms
from bootstrap_datepicker_plus import DateTimePickerInput
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone

from core.models import Auction


class AuctionCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.owner = kwargs.pop("owner")
        super().__init__(*args, **kwargs)

    class Meta:
        model = Auction
        fields = ['title', 'short_description', 'description', 'base_price', 'deadline', 'picture']
        widgets = {'deadline': DateTimePickerInput}

    def clean_deadline(self):
        data = self.cleaned_data['deadline']
        if data < timezone.now() + settings.MIN_AUCTION_TIME:
            raise ValidationError('The finish date should be some time after %d days from now'
                                  % settings.MIN_AUCTION_TIME.days)
        return data

    def clean_picture(self):
        data = self.cleaned_data['picture']
        print(data.size)
        return data

    def save(self, commit=True):
        auction = super().save(commit=False)
        auction.owner = self.owner
        if commit:
            auction.save()
        return auction
