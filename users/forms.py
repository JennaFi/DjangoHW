from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm

from catalog.forms import StyleFirmMixin
from users.models import User


class UserRegisterForm(StyleFirmMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']


class UserUpdateForm(StyleFirmMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ['email', 'phone', 'country', 'avatar']

