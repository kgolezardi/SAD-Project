from core.models import Report


def count(request):
    report_count = 0
    if request.user.is_authenticated:
        report_count = Report.objects.filter(read=False).count()
    return {'report_count': report_count,}
