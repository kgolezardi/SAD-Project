from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'core'
urlpatterns = [
    path('', TemplateView.as_view(template_name='core/home.html'), name='home'),
    path('auctions', views.auctions, name='auctions'),
    path('auctions/pending', views.pending_auctions_view, name='pending'),
    path('auctions/my', views.my_actions, name='my_auctions'),
    path('auctions/purchases', views.my_purchases, name='my_purchases'),
    path('auctions/create', views.AuctionCreateView.as_view(), name='create_auction'),
    path('auction/<int:auction_id>', views.description, name='description'),
    path('auction/<int:auction_id>/approve', views.approve_auction, name='approve'),
    path('auction/<int:auction_id>/reject', views.reject_auction, name='reject'),
    path('auction/<int:auction_id>/bid', views.offer_bid, name='bid'),
    path('auction/<int:auction_id>/receipt', views.confirm_receipt, name='receipt'),
    path('auction/<int:auction_id>/remove', views.remove_auction, name='remove_auction'),
    path('auction/<int:auction_id>/edit', views.AuctionEditView.as_view(), name='edit_auction'),
    path('auction/<int:auction_id>/image/<int:image_id>/delete', views.delete_image, name='delete_image'),
    path('auction/<int:auction_id>/report', views.report_auction, name='report_auction'),
    path('credit', views.credit, name='credit'),
    path('credit/charge', views.charge_credit, name='charge_credit'),
    path('credit/withdraw', views.withdraw_credit, name='withdraw_credit'),
    path('reports', views.show_reports, name='show_reports'),
    path('report/<int:report_id>', views.resolve, name='resolve_report'),
]
