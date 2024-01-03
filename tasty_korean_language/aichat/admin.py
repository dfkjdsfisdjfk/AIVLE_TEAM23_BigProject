from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(ChatLog)

class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('chatlog', 'sender', 'message', 'created_at')
    search_fields = ('sender', 'message')
    readonly_fields = ('created_at',)
    
admin.site.register(ChatMessage, ChatMessageAdmin)


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('chatmessage', 'accuracy', 'feedback', 'created_at', 'answer', 'created_at')
    search_fields = ('chatmessage', 'accuracy')
    readonly_fields = ('created_at',)
    
admin.site.register(Feedback, FeedbackAdmin)