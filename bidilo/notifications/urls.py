from django.urls import path

from . import views

app_name = 'notifications'
urlpatterns = [
    path('', views.show_notifs, name='show_notifs'),
    path('read/<int:notif_id>', views.read_notif, name='read_notif'),
    path('unread/<int:notif_id>', views.unread_notif, name='unread_notif'),
]
