from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView, ListView
from django.views.generic.edit import CreateView, UpdateView

from .forms import LabelForm
from .models import Label


class SuccessMessageMixin:
    success_message = ""

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.success_message:
            messages.success(self.request, self.success_message)
        return response


class LabelListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = "labels/index.html"
    context_object_name = "labels"


class LabelCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = "labels/form.html"
    success_url = reverse_lazy("labels:list")
    success_message = "Метка успешно создана."


class LabelUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = "labels/form.html"
    success_url = reverse_lazy("labels:list")
    success_message = "Метка успешно изменена."


class LabelDeleteView(LoginRequiredMixin, DeleteView):
    model = Label
    template_name = "labels/delete.html"
    success_url = reverse_lazy("labels:list")
    success_message = "Метка успешно удалена."
    protected_message = "Нельзя удалить метку, потому что она использована в задачах."

    def form_valid(self, form):
        self.object = self.get_object()
        success_url = self.get_success_url()
        if self.object.tasks.exists():
            messages.error(self.request, self.protected_message)
            return HttpResponseRedirect(success_url)
        self.object.delete()
        messages.success(self.request, self.success_message)
        return HttpResponseRedirect(success_url)
