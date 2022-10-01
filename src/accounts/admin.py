from django.contrib import admin
from django.contrib.admin.models import LogEntry

from .models import CustomUser


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ("action_flag", "object_repr", "user", "action_time", )


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "first_name", "last_name", "email", "date_joined",)



