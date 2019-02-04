from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import UserCreationForm, UserChangeForm
from .models import User, Supervisor, Customer


class CustomerAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ['email', 'username', ]


admin.site.register(User, CustomerAdmin)
admin.site.register(Customer)
admin.site.register(Supervisor)
