from django import forms

from .models import Task


class TaskForm(forms.ModelForm):
    name = forms.CharField(max_length=150, required=True, label="Имя")
    description = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 4}),
        required=False,
        label="Описание",
    )

    class Meta:
        model = Task
        fields = ("name", "description", "status", "executor")
