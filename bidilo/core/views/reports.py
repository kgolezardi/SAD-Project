from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from core.models import Report

def show_reports(request):
    reports = sorted(Report.objects.filter(read=False).order_by('-date'), key=lambda r: (r.reported_auction.report_count, r.reported_auction.id), reverse=True)
    return render(request, 'core/reports.html', context={"reports": reports})

def resolve(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    report.set_read()
    return HttpResponseRedirect(reverse('core:show_reports'))