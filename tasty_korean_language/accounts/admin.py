from django.contrib import admin
from .models import Profile, UserSession

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'address')
    search_fields = ('user__username', 'user__email', 'phone_number', 'address')

admin.site.register(Profile, ProfileAdmin)

class UserSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'session_key', 'created_at')
    search_fields = ('user__username', 'user__email', 'session_key')
    readonly_fields = ('created_at',)

admin.site.register(UserSession, UserSessionAdmin)