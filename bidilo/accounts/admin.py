from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomerCreationForm, CustomerChangeForm
from .models import User


class CustomerAdmin(UserAdmin):
    add_form = CustomerCreationForm
    form = CustomerChangeForm
    model = User
    list_display = ['email', 'username', ]


admin.site.register(User, CustomerAdmin)
