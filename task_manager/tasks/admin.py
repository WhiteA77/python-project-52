from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "status", "author", "executor", "created_at")
    search_fields = ("name", "description")
    list_filter = ("status", "author", "executor", "labels")
    filter_horizontal = ("labels",)
