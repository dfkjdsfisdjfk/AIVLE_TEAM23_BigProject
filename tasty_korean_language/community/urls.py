from django.urls import path
from . import views

app_name='community'

urlpatterns = [
    path('test1/', views.test1, name='index'),
    path('detail/<int:pk>', views.posting, name="detail"),
    path('write/', views.write, name='write'),    
]