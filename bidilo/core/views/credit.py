from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from core.forms import ChargeCreditForm
from core.forms import WithdrawCreditForm


@login_required
def credit(request):
    charge_form = ChargeCreditForm()
    withdraw_form = WithdrawCreditForm()
    return render(request, 'core/credit.html', {'charge_form': charge_form, 'withdraw_form': withdraw_form})


@login_required
def charge_credit(request):
    customer = request.user.customer
    if request.method == 'POST':
        form = ChargeCreditForm(request.POST)
        if form.is_valid():
            customer.credit += form.cleaned_data['charge_amount']
            customer.save()
    return HttpResponseRedirect(reverse('core:credit'))


@login_required
def withdraw_credit(request):
    customer = request.user.customer
    if request.method == 'POST':
        form = WithdrawCreditForm(request.POST)
        if form.is_valid():
            withdraw_amount = form.cleaned_data['withdraw_amount']
            if withdraw_amount <= customer.credit:
                customer.credit -= withdraw_amount
                customer.save()
            else:
                messages.error(request, "You can't withdraw more than your current credit.")
    return HttpResponseRedirect(reverse('core:credit'))
