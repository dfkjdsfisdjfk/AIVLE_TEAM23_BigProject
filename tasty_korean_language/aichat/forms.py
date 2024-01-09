from django import forms
from django.contrib.auth import get_user_model

class UserLanguageForm(forms.ModelForm):
    class Meta:
        model = get_user_model
        fields = ['language']