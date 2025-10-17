from unittest.mock import patch

from django.contrib.auth.models import User
from django.db.models import ProtectedError
from django.test import TestCase
from django.urls import reverse

from task_manager.tasks.models import Task

from ..models import Status


class StatusViewsTest(TestCase):
    def setUp(self):
        self.password = "StatusPass123!"
        self.user = User.objects.create_user(
            username="status_user",
            first_name="Status",
            last_name="User",
            password=self.password,
        )
        self.status = Status.objects.create(name="Новый")

    def test_list_requires_login(self):
        response = self.client.get(reverse("statuses:list"))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('statuses:list')}")

    def test_create_status(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("statuses:create"),
            data={"name": "В работе"},
        )
        self.assertRedirects(response, reverse("statuses:list"))
        self.assertTrue(Status.objects.filter(name="В работе").exists())

    def test_update_status(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("statuses:update", args=[self.status.pk]),
            data={"name": "Измененный"},
        )
        self.assertRedirects(response, reverse("statuses:list"))
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, "Измененный")

    def test_delete_status(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("statuses:delete", args=[self.status.pk]))
        self.assertRedirects(response, reverse("statuses:list"))
        self.assertFalse(Status.objects.filter(pk=self.status.pk).exists())

    def test_delete_status_protected(self):
        self.client.force_login(self.user)
        another_status = Status.objects.create(name="На тестировании")
        with patch.object(
            Status,
            "delete",
            side_effect=ProtectedError("protected", [another_status]),
        ):
            response = self.client.post(
                reverse("statuses:delete", args=[another_status.pk]),
                follow=True,
            )
        self.assertRedirects(response, reverse("statuses:list"))
        self.assertTrue(Status.objects.filter(pk=another_status.pk).exists())

    def test_delete_status_with_related_tasks_forbidden(self):
        self.client.force_login(self.user)
        task = Task.objects.create(
            name="Связанная задача",
            description="",
            status=self.status,
            author=self.user,
        )
        response = self.client.post(
            reverse("statuses:delete", args=[self.status.pk]),
            follow=True,
        )
        self.assertRedirects(response, reverse("statuses:list"))
        self.assertTrue(Status.objects.filter(pk=self.status.pk).exists())
        self.assertTrue(Task.objects.filter(pk=task.pk).exists())
