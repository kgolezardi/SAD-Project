from django.urls import reverse_lazy
from django.views import generic

from accounts.forms import CustomUserCreationForm
from accounts.models import User


class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'registration/signup.html'


class ProfileView(generic.UpdateView):
    model = User
    fields = ['name', 'address', 'phone_number']
    template_name = 'registration/edit_profile.html'
    success_url = reverse_lazy('core:home')

    def get_object(self, queryset=None):
        return self.request.user
