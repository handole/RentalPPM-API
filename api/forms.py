from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import master_employee


class SignUpForm(UserCreationForm):
    user_level = forms.CharField(max_length=10, required=True, help_text="Required. Maximum length is 10")
    user_type = forms.CharField(max_length=10, required=True, help_text="Required. Maximum length is 10")
    employee_id = forms.IntegerField(required=True)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'user_level', 'user_type', 'employee_id', )