from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Customer


class CustomerCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('name', 'username', 'email', 'address', 'phone_number')

    def save(self):
        user = super().save(commit=False)
        user.is_customer = True
        user.save()
        Customer.objects.create(user=user)
        return user


class CustomerChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('name', 'username', 'email', 'address', 'phone_number')

    def save(self):
        user = super().save()
        user.customer.save()
        return user
