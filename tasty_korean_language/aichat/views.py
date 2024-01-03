from django.shortcuts import render, redirect
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required

from .models import *

from openai import OpenAI

@login_required
def index(request):
    if (ChatLog.objects.filter(user=request.user).count() == 0):
        chatlog = ChatLog.objects.create(user=request.user)
    
    userchatlog = ChatLog.objects.filter(user=request.user).order_by('created_at').last()
    
    messages = ChatMessage.objects.filter(chatlog=userchatlog)
    return render(request, 'aichat/chat.html', {'messages': messages})


@login_required
def send(request):
    
    message = request.POST.get('message')
    sender = request.user.username
    
    chatlog = ChatLog.objects.filter(user=request.user).order_by('created_at').last()
    
    ChatMessage.objects.create(chatlog=chatlog, sender=sender, message=message)
    # response = get_chat_gpt_response(message)
    
    client = OpenAI(api_key="")

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": message}
        ]
    )
    
    response = completion.choices[0].message.content

    ChatMessage.objects.create(chatlog=chatlog, sender="system", message=response)

    return redirect('aichat:chat')
    


