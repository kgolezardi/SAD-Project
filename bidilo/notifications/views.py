from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404

from notifications.models import Notification


@login_required
def show_notifs(request):
    notifs = Notification.objects.filter(user=request.user).order_by('-date')
    return render(request, 'notifications/show_all.html', context={"notifs": notifs})


def read_notif(request, notif_id):
    notification = get_object_or_404(Notification, id=notif_id)
    if notification.user != request.user:
        return HttpResponseForbidden()
    notification.set_read()
    return HttpResponse('OK')


def unread_notif(request, notif_id):
    notification = get_object_or_404(Notification, id=notif_id)
    if notification.user != request.user:
        return HttpResponseForbidden()
    notification.set_unread()
    return HttpResponse('OK')