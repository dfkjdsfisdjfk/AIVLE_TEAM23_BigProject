from django.db import models
from django.conf import settings

class ChatLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.TextField(default = '제목없음')
    created_at = models.DateTimeField(auto_now_add=True)
    
    
class ChatMessage(models.Model):
    chatlog = models.ForeignKey(ChatLog, on_delete=models.CASCADE)
    sender = models.CharField(max_length=100)
    message = models.TextField()
    translated = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.message
    
    
class Feedback(models.Model):
    chatmessage = models.OneToOneField(ChatMessage, on_delete=models.CASCADE)
    accuracy = models.FloatField()
    accuracy_detail = models.FloatField()
    feedback = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    