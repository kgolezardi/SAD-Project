from bootstrap_datepicker_plus import DateTimePickerInput
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone

from core.models import Auction, auction_picture_validator, AuctionImage


class AuctionCreateForm(forms.ModelForm):
    small_images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}), label='Optionl images',
                                    help_text='The optional smaller images of the item', required=False)

    class Meta:
        model = Auction
        fields = ['title', 'short_description', 'description', 'base_price', 'deadline', 'picture', 'small_images']
        widgets = {'deadline': DateTimePickerInput}

    def __init__(self, *args, **kwargs):
        self.owner = kwargs.pop("owner")
        super().__init__(*args, **kwargs)

    def clean_deadline(self):
        data = self.cleaned_data['deadline']
        if data < timezone.now() + settings.MIN_AUCTION_TIME:
            raise ValidationError('The finish date should be some time after %d days from now'
                                  % settings.MIN_AUCTION_TIME.days)
        return data

    def clean_small_images(self):
        data = self.cleaned_data['small_images']
        for image in self.files.getlist('small_images'):
            auction_picture_validator(image)
        return data

    def save(self):
        auction = super().save(commit=False)
        auction.owner = self.owner
        auction.save()
        for image in self.files.getlist('small_images'):
            AuctionImage.objects.create(auction=auction, file=image)
        return auction
