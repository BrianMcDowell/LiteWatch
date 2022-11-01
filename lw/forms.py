from django import forms

from .models import Search


class NewSearchForm(forms.ModelForm):
    class Meta:
        model = Search
        exclude = ('user', 'dateCreated',)

