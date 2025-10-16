from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label="Имя")
    last_name = forms.CharField(max_length=150, required=True, label="Фамилия")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("first_name", "last_name", "username")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True, label="Имя")
    last_name = forms.CharField(max_length=150, required=True, label="Фамилия")

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username")


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150, required=True, label="Имя пользователя")
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput,
        label="Пароль",
    )
