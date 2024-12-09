import secrets
from pyexpat.errors import messages

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView

from config.settings import DEFAULT_FROM_EMAIL
from users.forms import UserRegisterForm, UserUpdateForm
from users.models import User


class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/user/email-confirm/{token}/"
        send_mail(subject="Подтверждение почты",
            message=f"Приветствуем тебя на нашем сайте! Перейди, пожалуйста, по ссылке для подтверждения почты {url}",
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
                  )
        return super().form_valid(form)

def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))



class UserUpdateProfile(UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'registration/profile_update.html'
    context_object_name = 'form'

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Profile updated successfully')
        return redirect(reverse('users:edit_profile'))

    def form_invalid(self, form):
        messages.error(self.request, 'Profile update failed')
        return redirect(reverse('users:edit_profile'))


