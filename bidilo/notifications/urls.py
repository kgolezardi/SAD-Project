from django.urls import path

from . import views

app_name = 'notifications'
urlpatterns = [
    path('', views.show_notifs, name='show_notifs'),
    path('read', views.read_notif, name='read_notif'),
    path('unread', views.unread_notif, name='unread_notif'),
]
