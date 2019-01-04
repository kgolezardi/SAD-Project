from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from core.forms import ChargeCreditForm


def charge_credit(request):
    user = request.user
    if request.method == 'POST':
        form = ChargeCreditForm(request.POST)
        if form.is_valid():
            user.credit += form.cleaned_data['charge_amount']
            user.save()
            return HttpResponseRedirect(reverse('core:home'))
        else:
            pass
    else:
        form = ChargeCreditForm()
    return render(request, 'core/charge_credit.html', {'form':form, 'user':user})

