from django import forms

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from django.contrib.auth import get_user_model

from .models import Task


class TaskForm(forms.ModelForm):
    name = forms.CharField(max_length=150, required=True, label="Имя")
    description = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 4}),
        required=False,
        label="Описание",
    )
    status = forms.ModelChoiceField(queryset=Status.objects.all(), label="Статус")
    executor = forms.ModelChoiceField(
        queryset=get_user_model().objects.all(),
        required=False,
        label="Исполнитель",
    )
    labels = forms.ModelMultipleChoiceField(
        queryset=Label.objects.all(),
        required=False,
        label="Метки",
        widget=forms.SelectMultiple(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Task
        fields = ("name", "description", "status", "executor", "labels")
