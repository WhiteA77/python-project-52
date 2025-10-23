from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django_filters.views import FilterView

from .forms import TaskForm
from .filters import TaskFilter
from .models import Task

class SuccessMessageMixin:
    success_message = ""

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.success_message:
            messages.success(self.request, self.success_message)
        return response


class AuthorRequiredMixin(LoginRequiredMixin):
    permission_message = "Удалять задачу может только её автор"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        task = self.get_object()
        if task.author_id != request.user.id:
            messages.error(request, self.permission_message)
            return HttpResponseRedirect(reverse_lazy("tasks:list"))
        return super().dispatch(request, *args, **kwargs)


class TaskListView(LoginRequiredMixin, FilterView):
    model = Task
    template_name = "tasks/index.html"
    context_object_name = "tasks"
    filterset_class = TaskFilter
    queryset = Task.objects.select_related("status", "author", "executor").prefetch_related("labels").order_by("pk")

    def get_filterset_kwargs(self, filterset_class):
        kwargs = super().get_filterset_kwargs(filterset_class)
        kwargs["request"] = self.request
        return kwargs


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "tasks/detail.html"
    context_object_name = "task"
    queryset = Task.objects.select_related("status", "author", "executor").prefetch_related("labels")


class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/form.html"
    success_url = reverse_lazy("tasks:list")
    success_message = "Задача успешно создана"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/form.html"
    success_url = reverse_lazy("tasks:list")
    success_message = "Задача успешно изменена"
    queryset = Task.objects.select_related("status", "author", "executor").prefetch_related("labels")


class TaskDeleteView(AuthorRequiredMixin, DeleteView):
    model = Task
    template_name = "tasks/delete.html"
    success_url = reverse_lazy("tasks:list")
    success_message = "Задача успешно удалена"
    queryset = Task.objects.select_related("status", "author", "executor").prefetch_related("labels")

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(request, self.success_message)
        return response

    def get_success_url(self):
        return self.success_url
