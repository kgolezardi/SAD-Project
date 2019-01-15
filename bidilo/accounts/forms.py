from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ('name', 'username', 'email', 'address', 'phone_number')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('name', 'username', 'email', 'address', 'phone_number')
