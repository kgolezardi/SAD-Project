from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from core.models import Report

def show_reports(request):
    reports = Report.objects.filter(read=False).order_by('-date')
    return render(request, 'core/reports.html', context={"reports": reports})

def resolve(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    report.set_read()
    return HttpResponseRedirect(reverse('core:description', args=(report.reported_auction.id,)))