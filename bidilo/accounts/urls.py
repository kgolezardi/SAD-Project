from django.urls import include
from django.urls import path

from accounts import views

app_name = 'accounts'
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('profile', views.ProfileView.as_view(), name='profile'),
    path('signup', views.CustomerSignUpView.as_view(), name='signup'),

]