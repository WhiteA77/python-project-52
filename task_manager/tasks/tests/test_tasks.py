from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from task_manager.statuses.models import Status

from ..models import Task


class TaskViewsTest(TestCase):
    def setUp(self):
        self.password = "TaskPass123!"
        self.author = User.objects.create_user(
            username="author",
            first_name="Author",
            last_name="User",
            password=self.password,
        )
        self.executor = User.objects.create_user(
            username="executor",
            first_name="Exec",
            last_name="User",
            password=self.password,
        )
        self.status = Status.objects.create(name="Новый")
        self.task = Task.objects.create(
            name="Первое дело",
            description="Описание задачи",
            status=self.status,
            author=self.author,
            executor=self.executor,
        )

    def test_list_requires_login(self):
        response = self.client.get(reverse("tasks:list"))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('tasks:list')}")

    def test_list_authenticated(self):
        self.client.force_login(self.author)
        response = self.client.get(reverse("tasks:list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task.name)

    def test_detail_requires_login(self):
        response = self.client.get(reverse("tasks:detail", args=[self.task.pk]))
        expected = f"{reverse('login')}?next={reverse('tasks:detail', args=[self.task.pk])}"
        self.assertRedirects(response, expected)

    def test_detail_authenticated(self):
        self.client.force_login(self.author)
        response = self.client.get(reverse("tasks:detail", args=[self.task.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task.name)

    def test_create_task(self):
        self.client.force_login(self.author)
        form_data = {
            "name": "Новая задача",
            "description": "Тестовое описание",
            "status": self.status.pk,
            "executor": self.executor.pk,
        }
        response = self.client.post(reverse("tasks:create"), data=form_data)
        self.assertRedirects(response, reverse("tasks:list"))
        task = Task.objects.get(name="Новая задача")
        self.assertEqual(task.author, self.author)

    def test_update_task(self):
        self.client.force_login(self.author)
        form_data = {
            "name": "Обновленное имя",
            "description": "Обновленное описание",
            "status": self.status.pk,
            "executor": self.executor.pk,
        }
        response = self.client.post(
            reverse("tasks:update", args=[self.task.pk]),
            data=form_data,
        )
        self.assertRedirects(response, reverse("tasks:list"))
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, "Обновленное имя")
        self.assertEqual(self.task.description, "Обновленное описание")

    def test_delete_task_by_author(self):
        self.client.force_login(self.author)
        response = self.client.post(reverse("tasks:delete", args=[self.task.pk]))
        self.assertRedirects(response, reverse("tasks:list"))
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())

    def test_delete_task_not_author_forbidden(self):
        other_user = User.objects.create_user(
            username="other",
            first_name="Other",
            last_name="User",
            password=self.password,
        )
        self.client.force_login(other_user)
        response = self.client.post(
            reverse("tasks:delete", args=[self.task.pk]),
            follow=True,
        )
        self.assertRedirects(response, reverse("tasks:list"))
        self.assertTrue(Task.objects.filter(pk=self.task.pk).exists())
