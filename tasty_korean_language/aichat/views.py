from django.shortcuts import render, redirect, resolve_url
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required

from .models import *

from openai import OpenAI

from django.conf import settings

@login_required
def index(request):
    chatlog = ChatLog.objects.create(user=request.user)
    
    return render(request, 'aichat/chat.html', {'messages': '', 'id': chatlog.id})


@login_required
def index2(request, id):
    userchatlog = ChatLog.objects.get(id=id)
    
    messages = ChatMessage.objects.filter(chatlog=userchatlog)
    return render(request, 'aichat/chat.html', {'messages': messages, 'id': id})


@login_required
def send(request, id):
    
    message = request.POST.get('message')
    sender = request.user.username
    
    chatlog = ChatLog.objects.get(id=id)
    
    ChatMessage.objects.create(chatlog=chatlog, sender=sender, message=message)
    # response = get_chat_gpt_response(message)
    
    gpt_key = settings.CHATGPT_API_KEY
    client = OpenAI(api_key=gpt_key)

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": message}
        ]
    )
    
    response = completion.choices[0].message.content

    ChatMessage.objects.create(chatlog=chatlog, sender="system", message=response)

    return redirect('aichat:chatlog', chatlog.id)
    


