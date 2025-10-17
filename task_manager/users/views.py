from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView, ListView, UpdateView
from django.views.generic.edit import CreateView

from .forms import UserLoginForm, UserRegisterForm, UserUpdateForm


class UserListView(ListView):
    model = User
    template_name = "users/index.html"
    context_object_name = "users"
    ordering = ("pk",)


class SuccessRedirectMixin:
    success_message = ""

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.success_message:
            messages.success(self.request, self.success_message)
        return response


class UserPermissionMixin(LoginRequiredMixin):
    permission_message = "У вас нет прав для изменения другого пользователя."

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)

        if self.get_object().pk != request.user.pk:
            messages.error(request, self.permission_message)
            return HttpResponseRedirect(reverse_lazy("users:list"))

        return super().dispatch(request, *args, **kwargs)


class UserCreateView(SuccessRedirectMixin, CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = "users/form.html"
    success_url = reverse_lazy("login")
    success_message = "Пользователь успешно зарегистрирован."


class UserUpdateView(UserPermissionMixin, SuccessRedirectMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "users/form.html"
    success_url = reverse_lazy("users:list")
    success_message = "Пользователь успешно изменен."


class UserDeleteView(UserPermissionMixin, DeleteView):
    model = User
    template_name = "users/delete.html"
    success_url = reverse_lazy("users:list")
    success_message = "Пользователь успешно удален."
    protected_message = "Нельзя удалить пользователя, потому что он связан с задачами."

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


class UserLoginView(LoginView):
    template_name = "login.html"
    authentication_form = UserLoginForm

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Вы вошли в систему.")
        return response

    def get_success_url(self):
        return self.get_redirect_url() or reverse_lazy("index")


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("index")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, "Вы вышли из системы.")
        return super().dispatch(request, *args, **kwargs)
