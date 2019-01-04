from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from core.forms import ChargeCreditForm
from core.forms import WithdrawCreditForm


@login_required
def credit(request):
    return render(request, 'core/credit.html')


@login_required
def charge_credit(request):
    user = request.user
    if request.method == 'POST':
        form = ChargeCreditForm(request.POST)
        if form.is_valid():
            user.credit += form.cleaned_data['charge_amount']
            user.save()
            return HttpResponseRedirect(reverse('core:credit'))
    else:
        form = ChargeCreditForm()
    return render(request, 'core/charge_credit.html', {'form': form})


@login_required
def withdraw_credit(request):
    user = request.user
    if request.method == 'POST':
        form = WithdrawCreditForm(request.POST)
        if form.is_valid():
            withdraw_amount = form.cleaned_data['withdraw_amount']
            if withdraw_amount <= user.credit:
                user.credit -= withdraw_amount
                user.save()
                return HttpResponseRedirect(reverse('core:credit'))
            else:
                form.add_error('withdraw_amount', "You can't withdraw more than your current credit.")
    else:
        form = WithdrawCreditForm()
    return render(request, 'core/withdraw_credit.html', {'form': form})
