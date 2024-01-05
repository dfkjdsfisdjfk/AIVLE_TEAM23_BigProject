from django.contrib.auth.forms import UserCreationForm 
from django import forms 
from .models import User
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.forms import ValidationError

class SignupForm(UserCreationForm):
        
        username = forms.CharField(
            label=('Username'),
            max_length=30,
            error_messages={
                'required': ('이 필드는 필수입니다..'),
                'unique': ('이미 사용중입니다.'),
            }
        )
        
        email = forms.EmailField(
            label=('이메일'),
            error_messages={
                'required': ('이 필드는 필수입니다.'),
                'invalid': ('유효한 이메일 주소를 입력하세요.'),
            }
        )
        
        # phone_number = forms.CharField()
        # address = forms.CharField()

        class Meta(UserCreationForm.Meta):
            model = get_user_model()
            fields = UserCreationForm.Meta.fields + ('email', )
            
        # 여기에 비밀번호 조건 등 추가 할 수 있음)    
        def clean_password2(self):
            password1 = self.cleaned_data.get("password1")
            password2 = self.cleaned_data.get("password2")

            if password1 and password2 and password1 != password2:
                raise ValidationError("비밀번호가 일치하지 않습니다.")

            if len(password2) < 8:
                raise ValidationError("비밀번호는 최소 8자 이상이어야 합니다.")
            

            return password2    