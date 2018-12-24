from django.urls import include
from django.urls import path

from accounts import views

app_name = 'accounts'
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('signup/', views.SignUp.as_view(), name='signup'),

]