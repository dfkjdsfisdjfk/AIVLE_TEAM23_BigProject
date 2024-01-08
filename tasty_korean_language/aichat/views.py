from django.shortcuts import render, redirect, resolve_url
from django.views.generic import ListView
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required

from .models import *

from openai import OpenAI

from django.conf import settings

from google.cloud import speech

from django.conf import settings
from django.core.files.storage import default_storage


#####################aichat#####################

@login_required
def index(request):
    chatlog = ChatLog.objects.create(user=request.user)
    
    # return redirect('aichat:chatlog', chatlog.id)
    return render(request, 'aichat/chat.html', {'messages': '', 'id': chatlog.id})

@login_required
def index2(request, id):
    userchatlog = ChatLog.objects.get(id=id)
    
    # messages = ChatMessage.objects.filter(chatlog=userchatlog)
    messages_with_feedback = ChatMessage.objects.filter(chatlog=userchatlog).select_related('feedback').all()
    
    print("index2 성공")
    
    return render(request, 'aichat/chat.html', {'messages': messages_with_feedback, 'id': id})


@login_required
def send(request, id):
    
    correct_message = request.POST.get('message')
    sender = request.user.username
    chatlog = ChatLog.objects.get(id=id)
    audio_file = request.FILES['audio_file']
    # audio_file = request.FILES.get('audio_file')
    # file_path = default_storage.save(sender+'/audio.mp3', audio_file)
    
    print(id)
    print(request.user)
    print(request.POST)
    print(request.FILES)
    print(correct_message)
    
    stt_message = run_stt(audio_file)
    ChatMessage.objects.create(chatlog=chatlog, sender=sender, message=stt_message)
    
    accurcy, feedback = get_pronunciation_feedback(stt_message, correct_message)
    Feedback.objects.create(chatmessage=ChatMessage.objects.last(), accuracy=accurcy, feedback=feedback, answer=correct_message)
    
    chat_gpt_response = get_chat_gpt_response(correct_message)
    ChatMessage.objects.create(chatlog=chatlog, sender="system", message=chat_gpt_response)

    # return redirect('aichat:chatlog', chatlog.id)
    return redirect('aichat:chatlog', id)
    
#####################함수#####################

def run_stt(audio_file):
    client = speech.SpeechClient()
    
    audio = speech.RecognitionAudio(content=audio_file.read())
    
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3,
        sample_rate_hertz=36000,
        language_code="ko-KR",
    )
    
    response = client.recognize(config=config, audio=audio)
    
    for result in response.results:
        print("Transcript: {}".format(result.alternatives[0].transcript))
    
    return response.results[0].alternatives[0].transcript
     
     
def get_chat_gpt_response(message):
    
    client = OpenAI(api_key=settings.CHATGPT_API_KEY)

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": message}
        ]
    )
    
    response = completion.choices[0].message.content
    
    return response

def get_pronunciation_feedback(stt_message, correct_message):
    
    return 0.5, "good job"



#####################chatlog list#####################

class ChatLogListView(ListView):
    model = ChatLog
    template_name = 'aichat/chatlog_list.html'
    context_object_name = 'chatlog_list'

    def get_queryset(self):
        # Fetch all ChatLogs with their first ChatMessage
        return ChatLog.objects.prefetch_related('chatmessage_set').annotate(first_message=models.Min('chatmessage__created_at'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add any additional context data if needed
        return context











# def run_stt_by_gcs():
#     client = speech.SpeechClient()
    
#     # gcs_uri = "gs://kt-tkl/712826a6-d075-46d6-bea3-c88471b27cef.wav"
#     gcs_uri = "gs://kt-tkl/712826a6-d075-46d6-bea3-c88471b27cef.mp3"
    
#     audio = speech.RecognitionAudio(uri=gcs_uri)
    
#     config = speech.RecognitionConfig(
#         encoding=speech.RecognitionConfig.AudioEncoding.MP3,
#         sample_rate_hertz=36000,
#         language_code="ko-KR",
#     )
    
#     operation = client.long_running_recognize(config=config, audio=audio)
    
#     print("Waiting for operation to complete...")
#     response = operation.result(timeout=90)
    
#     print(response)
    
#     # for result in response.results:
#     #     print("Transcript: {}".format(result.alternatives[0].transcript))
    
    
#     return response.results[0].alternatives[0].transcript
