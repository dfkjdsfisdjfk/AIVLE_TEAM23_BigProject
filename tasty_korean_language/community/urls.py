from django.urls import path
from . import views

app_name='community'

urlpatterns = [
    path('test1/', views.test1),
    path('detail/<int:pk>', views.posting, name="detail"),    
]