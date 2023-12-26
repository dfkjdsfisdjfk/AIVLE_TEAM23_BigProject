from django.urls import path
from . import views

urlpatterns = [
     path('login/', views.login, name='login'),
     path('signup1/', views.signup1, name='signup'),
     path('signup2/', views.signup2, name='signup2'),
]
