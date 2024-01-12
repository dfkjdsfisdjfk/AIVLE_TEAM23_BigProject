from django.db import models
from django.conf import settings
from django.core.mail import send_mail 
from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    LANGUAGE_CHOICES = (
        ("en", "English"),
        ("ko", "Korean"),
        ("ja", "Japanese"),
        ("zh", "Chinese"),
    )
    
    language = models.CharField(choices=LANGUAGE_CHOICES, max_length=2, default="en")


from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth.signals import user_logged_in

class UserSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)

def block_duplicate_login(sender, request, user, **kwargs):
    login_user_list = UserSession.objects.filter(user=user)
    
    for user_session in login_user_list:
        session = SessionStore(user_session.session_key)
        # session.delete()
        session['blocked'] = True
        session.save()
    
    session_key = request.session.session_key
    UserSession.objects.create(user=user, session_key = session_key)

user_logged_in.connect(block_duplicate_login)