from notifications.models import Notification


def count(request):
    c = Notification.objects.filter(user=request.user, read=False).count()
    return {'notification_count': c}
