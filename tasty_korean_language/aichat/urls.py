from django.urls import path
from django.views.generic import TemplateView
from . import views 

app_name = 'aichat'

urlpatterns = [   
    # path('chat/', TemplateView.as_view(template_name='aichat/chat.html'), name='chat'),  
    path('', views.index, name='chat'),
    path('<int:id>/', views.index2, name='chatlog'),
    path('send/<int:id>/', views.send, name='send'),
    path('translate/', views.translate, name='translate'),
    path('update_language/', views.update_language, name='update_language'),
]