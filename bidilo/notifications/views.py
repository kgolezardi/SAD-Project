from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from notifications.models import Notification


@login_required
def show_notifs(request):
    notifs = Notification.objects.filter(user=request.user).order_by('-date')
    return render(request, 'notifications/show_all.html', context={"notifs": notifs})


def read_notif(request):
    notif_id = request.POST.get('notif_id', -1)
    notification = get_object_or_404(Notification, id=notif_id)
    if notification.user != request.user:
        return HttpResponseForbidden()
    notification.set_read()
    data = {'done': True}
    return JsonResponse(data)


def unread_notif(request):
    notif_id = request.POST.get('notif_id', -1)
    notification = get_object_or_404(Notification, id=notif_id)
    if notification.user != request.user:
        return HttpResponseForbidden()
    notification.set_unread()
    data = {'done': True}
    return JsonResponse(data)
