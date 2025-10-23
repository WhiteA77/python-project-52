from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin


class LoginMessageRequiredMixin(LoginRequiredMixin):

    login_message = "Вы не авторизованы! Пожалуйста, выполните вход."

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.error(self.request, self.login_message)
        return super().handle_no_permission()
