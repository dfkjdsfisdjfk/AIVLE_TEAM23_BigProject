from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from .forms import SignupForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

# from aichat.models import ChatLog, ChatMessage
from aichat.models import *
from community.models import Post


def signupConsent(request):
    return render(request, 'registration/signup_consent.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(settings.LOGIN_URL)            
    else:
        form = SignupForm()

    return render(request, 'registration/signup.html',{'form':form})


def findID(request):
    if request.method == 'POST':
        User = get_user_model()
        email = request.POST.get('email', None)
        if email:
            try:
                user = User.objects.get(email=email)
                return JsonResponse({'result': user.username})
            except User.DoesNotExist:
                return JsonResponse({'result': 'User not found'})
    return JsonResponse({}, status=400)

def custom_password_reset(request):
    return PasswordResetView.as_view(
        template_name='passsword_reset_form.html',  # 여러분의 템플릿 경로를 제공하세요
        success_url=reverse_lazy('password_reset_done'),
        email_template_name='your_email_template.html',  # 선택적으로 사용자 정의 이메일 템플릿을 만들 수 있습니다.
    )(request)

def custom_password_reset_done(request):
    return PasswordResetDoneView.as_view(
        template_name='your_password_reset_done_template.html',  # 여러분의 템플릿 경로를 제공하세요
    )(request)

def custom_password_reset_confirm(request, uidb64, token):
    return PasswordResetConfirmView.as_view(
        template_name='passsword_reset_confirm.html',  # 여러분의 템플릿 경로를 제공하세요
        success_url=reverse_lazy('password_reset_complete'),
    )(request, uidb64=uidb64, token=token)

def custom_password_reset_complete(request):
    return PasswordResetCompleteView.as_view(
        template_name='your_password_reset_complete_template.html',  # 여러분의 템플릿 경로를 제공하세요
    )(request)


class MyPasswordChangeView(PasswordChangeView) :
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        messages.info(self.request, '암호 변경을 완료했습니다!')
        return super().form_valid(form)
    


# Cookie Test 
def cookie_test(request, code):
    response = render(request, 'registration/cookieTest.html')
    if code == 'add':
        response.set_cookie('model', 'A001')
        response.set_cookie('prod', 'EV9')
    elif code == 'get' :
        model = request.COOKIES.get('model')
        prod = request.COOKIES.get('prod')
        print(model, prod)
    elif code == 'del' :
        response.delete_cookie('model')
        response.delete_cookie('prod')
    return response
        

from django.contrib.sessions.backends.db import SessionStore

# Session Test
def session_test(request, code):
    response = render(request, 'registration/sessionTest.html')
    session = request.session
    if code == 1:
        user = request.user        
        print(user,':', session)
    elif code == 2 :        
        session['model'] = 'A001'
        session['prod'] = 'EV9'
        print('session 데이터 등록')
    elif code == 3:
        model = session.get('model')
        prod = session.get('prod')
        print('session 데이터 추출')
        print(model, prod)
    elif code == 4:
        session.pop('model')
        print('session 데이터 삭제')
        session.pop('prod')
    return response    


###################### mypage ######################
def mypage(request):
    chatlog_list = ChatLog.objects.filter(user=request.user)
    post_list = Post.objects.filter(writer=request.user).order_by("-create_date")
    return render(request, 'registration/mypage.html', {'chatlog_list':chatlog_list, 'post_list':post_list})

