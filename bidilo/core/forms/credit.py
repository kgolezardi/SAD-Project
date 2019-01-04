from django import forms

class ChargeCreditForm(forms.Form):
    charge_amount = forms.IntegerField(min_value=5000, max_value=5000000)
