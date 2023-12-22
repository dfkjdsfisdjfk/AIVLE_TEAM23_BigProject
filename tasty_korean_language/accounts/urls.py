from django.urls import path
from . import views

urlpatterns = [
     path('login/', views.login),
     path('signup1/', views.signup1),
     path('signup2/', views.signup2),
]
