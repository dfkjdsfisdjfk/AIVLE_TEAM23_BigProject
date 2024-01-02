from django.contrib import admin
from .models import ChatMessage

# Register your models here.

class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'created_at')
    search_fields = ('user', 'message')
    readonly_fields = ('created_at',)
    
admin.site.register(ChatMessage, ChatMessageAdmin)
