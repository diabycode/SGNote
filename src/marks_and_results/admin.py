from django.contrib import admin

from .models import Mark


@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    list_display = ("student", "lesson", "semester", "mark_type", )

