from django.urls import path

from . import views

app_name = 'core'
urlpatterns = [
    path('auctions', views.auctions, name='auctions'),
    path('auction/<int:auction_id>', views.description, name='description')
]