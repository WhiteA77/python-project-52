from django import forms
from django.contrib.auth import get_user_model
import django_filters

from task_manager.labels.models import Label
from task_manager.statuses.models import Status

from .models import Task
from .forms import FullNameModelChoiceField

User = get_user_model()


class FullNameModelChoiceFilter(django_filters.ModelChoiceFilter):
    field_class = FullNameModelChoiceField


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        label="Статус",
        queryset=Status.objects.all(),
        empty_label="---------",
    )
    executor = FullNameModelChoiceFilter(
        label="Исполнитель",
        queryset=User.objects.all(),
        empty_label="---------",
    )
    labels = django_filters.ModelChoiceFilter(
        label="Метка",
        queryset=Label.objects.all(),
        empty_label="---------",
    )
    my_tasks = django_filters.BooleanFilter(
        label="Только свои задачи",
        method="filter_my_tasks",
        widget=forms.CheckboxInput(),
    )

    class Meta:
        model = Task
        fields = ("status", "executor", "labels")

    def __init__(self, data=None, queryset=None, *, request=None, prefix=None):
        super().__init__(data=data, queryset=queryset, request=request, prefix=prefix)
        self.request = request

    def filter_my_tasks(self, queryset, name, value):
        if value and self.request and self.request.user.is_authenticated:
            return queryset.filter(author=self.request.user)
        return queryset
