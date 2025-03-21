from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm

from .models import Room, User


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = ['topic', 'name', 'description']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'bio', 'username', 'email']
