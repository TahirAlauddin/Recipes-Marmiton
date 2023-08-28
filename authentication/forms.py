from allauth.account.forms import SignupForm
from django.contrib.auth import get_user_model
from django import forms

User = get_user_model()

class CustomSignupForm(SignupForm):
    birth_date = forms.DateField(label='Birth Date')
    