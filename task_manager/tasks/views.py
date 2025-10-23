from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django_filters.views import FilterView

from .forms import TaskForm
from .filters import TaskFilter
from .models import Task
from task_manager.mixins import LoginMessageRequiredMixin

class SuccessMessageMixin:
    success_message = ""

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.success_message:
            messages.success(self.request, self.success_message)
        return response


class AuthorRequiredMixin(LoginMessageRequiredMixin):
    permission_message = "Удалять задачу может только её автор"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        task = self.get_object()
        if task.author_id != request.user.id:
            messages.error(request, self.permission_message)
            return HttpResponseRedirect(reverse_lazy("tasks:list"))
        return super().dispatch(request, *args, **kwargs)


class TaskListView(LoginMessageRequiredMixin, FilterView):
    model = Task
    template_name = "tasks/index.html"
    context_object_name = "tasks"
    filterset_class = TaskFilter
    queryset = Task.objects.select_related("status", "author", "executor").prefetch_related("labels").order_by("pk")

    def get_filterset_kwargs(self, filterset_class):
        kwargs = super().get_filterset_kwargs(filterset_class)
        kwargs["request"] = self.request
        return kwargs


class TaskDetailView(LoginMessageRequiredMixin, DetailView):
    model = Task
    template_name = "tasks/detail.html"
    context_object_name = "task"
    queryset = Task.objects.select_related("status", "author", "executor").prefetch_related("labels")


class TaskCreateView(LoginMessageRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/form.html"
    success_url = reverse_lazy("tasks:list")
    success_message = "Задача успешно создана"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginMessageRequiredMixin, SuccessMessageMixin, UpdateView):
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
        messages.success(request, self.success_message)
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return self.success_url
