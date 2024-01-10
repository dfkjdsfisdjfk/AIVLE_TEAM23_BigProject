from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from django.views.generic import TemplateView
from django.contrib import admin


urlpatterns = [     
     path('login/', auth_views.LoginView.as_view(), name='login'),
     path('logout/', auth_views.LogoutView.as_view(), name='logout'),
     path('signup_consent/', views.signupConsent, name='signup_consent'),
     path('signup/', views.signup, name='signup'),
     path("id_find/", TemplateView.as_view(template_name='registration/id_find.html'), name="id_find"),
     path("id_find/find/", views.findID, name="find_id_by_email"),
     path(
          "password_change_form/", views.MyPasswordChangeView.as_view(), name="password_change"
     ),
     path(
          "password_change/done/",
          auth_views.PasswordChangeDoneView.as_view(),
          name="password_change_done",
     ),

    path('cookie/<code>/', views.cookie_test),
    
    path('session/<int:code>', views.session_test),
     
#     path('mypage/', TemplateView.as_view(template_name='registration/mypage.html'), name='mypage'),

    path('mypage/', views.mypage, name='mypage'),

]
