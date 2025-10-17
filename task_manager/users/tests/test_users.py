from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from task_manager.statuses.models import Status
from task_manager.tasks.models import Task


class UserViewsTest(TestCase):
    def setUp(self):
        self.password = "Secret123!"
        self.user = User.objects.create_user(
            username="hexlet",
            first_name="Hex",
            last_name="Let",
            password=self.password,
        )

    def test_user_list_available(self):
        other = User.objects.create_user(
            username="user2",
            first_name="User",
            last_name="Two",
            password="AnotherPass123!",
        )
        response = self.client.get(reverse("users:list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)
        self.assertContains(response, other.username)

    def test_user_create(self):
        form_data = {
            "first_name": "New",
            "last_name": "User",
            "username": "newuser",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
        }
        response = self.client.post(reverse("users:create"), data=form_data)
        self.assertRedirects(response, reverse("login"))
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_user_update_self(self):
        self.client.force_login(self.user)
        form_data = {
            "first_name": "Updated",
            "last_name": "Name",
            "username": self.user.username,
        }
        response = self.client.post(
            reverse("users:update", args=[self.user.pk]),
            data=form_data,
        )
        self.assertRedirects(response, reverse("users:list"))
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Updated")
        self.assertEqual(self.user.last_name, "Name")

    def test_user_update_forbidden_for_others(self):
        other = User.objects.create_user(
            username="hacker",
            first_name="Bad",
            last_name="User",
            password="StrongPass123!",
        )
        self.client.force_login(other)
        form_data = {
            "first_name": "Hack",
            "last_name": "Attempt",
            "username": self.user.username,
        }
        response = self.client.post(
            reverse("users:update", args=[self.user.pk]),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(response, reverse("users:list"))
        self.user.refresh_from_db()
        self.assertNotEqual(self.user.first_name, "Hack")

    def test_user_delete_self(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("users:delete", args=[self.user.pk]))
        self.assertRedirects(response, reverse("users:list"))
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())

    def test_user_delete_forbidden_for_others(self):
        other = User.objects.create_user(
            username="intruder",
            first_name="Intru",
            last_name="Der",
            password="StrongPass123!",
        )
        self.client.force_login(other)
        response = self.client.post(
            reverse("users:delete", args=[self.user.pk]),
            follow=True,
        )
        self.assertRedirects(response, reverse("users:list"))
        self.assertTrue(User.objects.filter(pk=self.user.pk).exists())

    def test_user_delete_blocked_when_related_tasks(self):
        status = Status.objects.create(name="Статус для теста")
        Task.objects.create(
            name="Связанная задача",
            description="",
            status=status,
            author=self.user,
        )
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("users:delete", args=[self.user.pk]),
            follow=True,
        )
        self.assertRedirects(response, reverse("users:list"))
        self.assertTrue(User.objects.filter(pk=self.user.pk).exists())

    def test_login_success_redirects_home(self):
        response = self.client.post(
            reverse("login"),
            data={"username": self.user.username, "password": self.password},
        )
        self.assertRedirects(response, reverse("index"))

    def test_logout_redirects_home(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("logout"))
        self.assertRedirects(response, reverse("index"))
