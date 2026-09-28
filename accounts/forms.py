from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class RegisterForm(UserCreationForm):
    role = forms.ChoiceField(choices=[(User.Role.FARMER, "Farmer"), (User.Role.CUSTOMER, "Customer")])
    phone = forms.CharField(max_length=15, required=False)

    class Meta:
        model = User
        fields = ["username", "email", "phone", "role", "password1", "password2"]
