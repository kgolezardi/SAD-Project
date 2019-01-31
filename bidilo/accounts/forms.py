from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Customer

class CustomerCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('name', 'username', 'email', 'address', 'phone_number')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_customer = True
        if commit:
            user.save()
        customer = Customer(user=user)
        if commit:
            customer.save()
        return user


class CustomerChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('name', 'username', 'email', 'address', 'phone_number')

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            user.customer.save()
        return user
