from django.contrib import admin
from .models import User, UserSession

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'language', 'is_staff', 'is_active', 'last_login', 'date_joined')
    search_fields = ('user__username', 'user__email')

admin.site.register(User, UserAdmin)

class UserSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'session_key', 'created_at')
    search_fields = ('user__username', 'user__email', 'session_key')
    readonly_fields = ('created_at',)

admin.site.register(UserSession, UserSessionAdmin)