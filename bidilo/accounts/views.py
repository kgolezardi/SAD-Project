from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.views import generic

from accounts.forms import UserCreationForm
from accounts.models import User


class CustomerSignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'registration/signup.html'


class SupervisorSignUpView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('core:home')
    template_name = 'registration/signup.html'

    def test_func(self):
        return self.request.user.is_superuser

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['supervisor'] = True
        return kwargs


class ProfileView(generic.UpdateView):
    model = User
    fields = ['name', 'address', 'phone_number']
    template_name = 'registration/edit_profile.html'
    success_url = reverse_lazy('core:home')

    def get_object(self, queryset=None):
        return self.request.user
