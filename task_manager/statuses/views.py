from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView, ListView
from django.views.generic.edit import CreateView, UpdateView

from .forms import StatusForm
from .models import Status


class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = "statuses/index.html"
    context_object_name = "statuses"


class SuccessMessageMixin:
    success_message = ""

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.success_message:
            messages.success(self.request, self.success_message)
        return response


class StatusCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = "statuses/form.html"
    success_url = reverse_lazy("statuses:list")
    success_message = "Статус успешно создан."


class StatusUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = "statuses/form.html"
    success_url = reverse_lazy("statuses:list")
    success_message = "Статус успешно изменен."


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = "statuses/delete.html"
    success_url = reverse_lazy("statuses:list")
    success_message = "Статус успешно удален."
    protected_message = "Нельзя удалить статус, потому что он используется."

    def form_valid(self, form):
        self.object = self.get_object()
        success_url = self.get_success_url()
        try:
            self.object.delete()
        except ProtectedError:
            messages.error(self.request, self.protected_message)
            return HttpResponseRedirect(success_url)
        messages.success(self.request, self.success_message)
        return HttpResponseRedirect(success_url)
