from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task


class LabelViewsTest(TestCase):
    def setUp(self):
        self.password = "LabelPass123!"
        self.user = User.objects.create_user(
            username="label_user",
            first_name="Label",
            last_name="User",
            password=self.password,
        )
        self.label = Label.objects.create(name="bug")
        self.status = Status.objects.create(name="Новый")

    def test_list_requires_login(self):
        response = self.client.get(reverse("labels:list"))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('labels:list')}")

    def test_list_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("labels:list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.label.name)

    def test_create_label(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("labels:create"),
            data={"name": "feature"},
        )
        self.assertRedirects(response, reverse("labels:list"))
        self.assertTrue(Label.objects.filter(name="feature").exists())

    def test_update_label(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("labels:update", args=[self.label.pk]),
            data={"name": "bugfix"},
        )
        self.assertRedirects(response, reverse("labels:list"))
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, "bugfix")

    def test_delete_label(self):
        self.client.force_login(self.user)
        label = Label.objects.create(name="temp")
        response = self.client.post(reverse("labels:delete", args=[label.pk]))
        self.assertRedirects(response, reverse("labels:list"))
        self.assertFalse(Label.objects.filter(pk=label.pk).exists())

    def test_delete_label_protected(self):
        self.client.force_login(self.user)
        task = Task.objects.create(
            name="Task with label",
            description="",
            status=self.status,
            author=self.user,
        )
        task.labels.add(self.label)
        response = self.client.post(
            reverse("labels:delete", args=[self.label.pk]),
            follow=True,
        )
        self.assertRedirects(response, reverse("labels:list"))
        self.assertTrue(Label.objects.filter(pk=self.label.pk).exists())
