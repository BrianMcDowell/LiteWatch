from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Search


class NewSearchForm(forms.ModelForm):
    """New search form"""

    class Meta:
        model = Search
        exclude = ('user', 'dateCreated',)


class UserRegisterForm(UserCreationForm):
    """New user form"""

    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
