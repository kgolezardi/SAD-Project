from notifications.models import Notification


def count(request):
    c = 0
    if request.user.is_authenticated:
        c = Notification.objects.filter(user=request.user, read=False).count()
    return {'notification_count': c}
