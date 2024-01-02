from django.shortcuts import render, redirect
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required

from .models import ChatMessage

from openai import OpenAI

@login_required
def index(request):
    messages = ChatMessage.objects.all()
    return render(request, 'aichat/chat.html', {'messages': messages})


@login_required
def send(request):
    
    message = request.POST.get('message')
    user = request.user.username

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

    message = ChatMessage(user=user, message=response)
    message.save()

    return redirect('aichat:chat')
    


