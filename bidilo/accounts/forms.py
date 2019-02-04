from django.contrib.auth import forms
from .models import User, Customer, Supervisor


class UserCreationForm(forms.UserCreationForm):
    class Meta(forms.UserCreationForm.Meta):
        model = User
        fields = ('name', 'username', 'email', 'address', 'phone_number')

    def __init__(self, *args, **kwargs):
        self.supervisor = kwargs.pop('supervisor', False)
        super().__init__(*args, **kwargs)

    def save(self):
        user = super().save(commit=False)
        if self.supervisor:
            user.is_supervisor = True
        else:
            user.is_customer = True
        user.save()
        if self.supervisor:
            Supervisor.objects.create(user=user)
        else:
            Customer.objects.create(user=user)
        return user


class UserChangeForm(forms.UserChangeForm):
    class Meta(forms.UserChangeForm.Meta):
        model = User
        fields = ('name', 'username', 'email', 'address', 'phone_number')

    def save(self):
        user = super().save()
        return user
