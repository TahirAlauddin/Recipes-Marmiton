from django.db.models.fields import EmailField
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=60, widget=forms.TextInput({'placeholder': 'Add a valid email'}))

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'username')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields