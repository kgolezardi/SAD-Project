from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'core'
urlpatterns = [
    path('', TemplateView.as_view(template_name='core/home.html'), name='home'),
    path('auctions', views.auctions, name='auctions'),
    path('auction/<int:auction_id>', views.description, name='description')
]