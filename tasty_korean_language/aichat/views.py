from django.shortcuts import render, redirect, resolve_url
from django.views.generic import ListView
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required

from .models import *

from openai import OpenAI

from django.conf import settings

from google.cloud import speech

from django.conf import settings
from django.core.files.storage import FileSystemStorage, default_storage, Storage


import urllib3
import json
import base64
import librosa
import numpy as np

import random
import json



import urllib3
import json
import base64
# import librosa
import numpy as np


from pydub import AudioSegment

import os


#####################aichat#####################
from google.cloud import translate_v2
from .STT import etri_eval, compare, hug_stt_acc, etri_stt


# Lanugae 설정 Update
def update_language(request):
    if request.method == 'PATCH':
        data = json.loads(request.body)
        language = data.get('language')
        request.user.language = language
        request.user.save()
        return JsonResponse({'message': 'Language updated successfully!'})

    return JsonResponse({'error': 'Invalid request method.'}, status=400)


@login_required
def chatsetting(request):
    chatloglist = ChatLog.objects.filter(user=request.user)
    
    return render(request, 'aichat/chat_setting.html', {'chatloglist': chatloglist})


@login_required
def index(request):
    chatlog = ChatLog.objects.create(user=request.user)
    
    
    initial_gpt_message = get_chat_gpt_response("이야기!")  # 초기 메시지를 GPT에 전달
    ChatMessage.objects.create(chatlog=chatlog, sender="system", message=initial_gpt_message)
    
    return redirect('aichat:chatlog', chatlog.id)
    # return render(request, 'aichat/chat.html', {'messages': '', 'id': chatlog.id})

@login_required
def index2(request, id):
    userchatlog = ChatLog.objects.get(id=id)
    
    # messages = ChatMessage.objects.filter(chatlog=userchatlog)
    messages_with_feedback = ChatMessage.objects.filter(chatlog=userchatlog).select_related('feedback').all()
    
    print("index2 성공")
    
    return render(request, 'aichat/chat.html', {'messages': messages_with_feedback, 'id': id})

@login_required
def send(request, id):
    
    # correct_message = request.POST.get('message')
    correct_message = request.POST.get('message')
    sender = request.user.username
    chatlog = ChatLog.objects.get(id=id)
    
    # try:
    #     audio_file = request.FILES['audio_file']
    # except MultiValueDictKeyError:
    #     return JsonResponse({'error': 'audio_file key not found'}, status=400)
    audio_file = request.FILES['audio_file']
    # audio_file = request.FILES.get('audio_file')
    
    print(id)
    print(request.user)
    print(request.POST)
    print(request.FILES)
    print(correct_message)
    
    stt_message = run_stt(audio_file)
    ChatMessage.objects.create(chatlog=chatlog, sender=sender, message=stt_message)
    # userchatmessage = ChatMessage.objects.create(chatlog=chatlog, sender=sender, message=stt_message)
    
    last_chatmessage_id = ChatMessage.objects.last().id
    default_storage.save(sender+'/' + str(last_chatmessage_id) + '.webm', audio_file)
    # default_storage.save( 'record_file/ + 'f'{sender}_' + str(last_chatmessage_id) + '.webm', audio_file)
    # file_path = default_storage.save(sender+'/' + ' ' + '.mp3', audio_file)
    
    detail_acc, accurcy, feedback = get_pronunciation_feedback(correct_message, audio_file, sender,last_chatmessage_id)

    Feedback.objects.create(chatmessage=ChatMessage.objects.last(), accuracy_detail = detail_acc, accuracy=accurcy, feedback=feedback, answer=correct_message)
    
    chat_gpt_response = get_chat_gpt_response(correct_message)
    ChatMessage.objects.create(chatlog=chatlog, sender="system", message=chat_gpt_response)

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
            {"role": "system", "content": "I am small talker."},
            {"role": "user", "content": message}
        ]
    )
    
    response = completion.choices[0].message.content
    
    return response


# def get_pronunciation_feedback(origin_text:str,audio):
def get_pronunciation_feedback(origin_text,audio,sender,last_chatmessage_id):
    # etri 키 불러오기
    key = settings.ETRI_API_KEY
    audioFilePath = ".\\media\\" + sender + "\\" + str(last_chatmessage_id) + ".webm"
    
    # make dir
    current_path = os.getcwd()
    if not os.path.exists(current_path + "\\media\\" + sender + "_transformed"):
        os.mkdir(current_path + "\\media\\" + sender + "_transformed")
    
    saveFilePath = ".\\media\\" + sender + "_transformed" + "\\" + str(last_chatmessage_id) + ".wav"

    
    webm = AudioSegment.from_file(audioFilePath, format="webm")
    print(2)
    webm.export(saveFilePath, format="wav")
    
    # 평가 모듈을 사용하여 평가
    STT_result, hug_acc = hug_stt_acc(origin_text, saveFilePath)
    stt_etri = etri_stt(saveFilePath,key)
    etri_score = etri_eval(origin_text,saveFilePath,key)
    compare_lt = compare(origin_text, STT_result)
    to_compare_lt_str = ", ".join(sum(compare_lt, []))
    
    print(STT_result)
    print(stt_etri)
    print(hug_acc)
    print(etri_score)
    print(compare_lt)
    
    
    return hug_acc, etri_score, to_compare_lt_str


###############################################################################################
def translate(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        message = request.POST.get('message')
        target_language = 'ko'  # 대상 언어 설정

        # 번역 수행
        translation_client = translate_v2.Client.from_service_account_json("C:\\Users\\user\\Desktop\\chat.json")
        translated_message = translation_client.translate(message, target_language=target_language)['translatedText']
        
        return JsonResponse({'translated_message': translated_message})
    else:
        return JsonResponse({'error': '잘못된 요청'}, status=400)

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
        
