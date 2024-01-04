from django.contrib.auth.forms import UserCreationForm 
from django import forms 
from .models import User
from django.contrib.auth import get_user_model

class SignupForm(UserCreationForm):
    # phone_number = forms.CharField()
    # address = forms.CharField()

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ('email', )

    # def save(self):
    #     user = super().save() 
    #     # Profile.objects.create(user=user, 
    #     #                        phone_number=self.cleaned_data['phone_number'],
    #     #                        address=self.cleaned_data['address'])
    #     User.objects.create(user=user)
    #     return user