from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from tasks.models import Position, Worker, TaskType, Task


class WorkerModelTest(TestCase):

    def setUp(self):
        self.position = Position.objects.create(name="Developer")

        self.worker = Worker.objects.create_user(
            username="john",
            first_name="John",
            last_name="Smith",
            position=self.position,
        )

    def test_str_method(self):
        self.assertEqual(str(self.worker), "john (John Smith)")

    def test_get_absolute_url(self):
        expected_url = reverse(
            "tasks:worker-detail", kwargs={"pk": self.worker.pk}
        )

        self.assertEqual(self.worker.get_absolute_url(), expected_url)


class TaskModelTest(TestCase):

    def setUp(self):
        self.task_type = TaskType.objects.create(name="Development")

        self.task = Task.objects.create(
            name="Create API",
            description="Develop a REST API",
            deadline=timezone.now() + timedelta(days=7),
            priority="3",
            task_type=self.task_type,
        )

    def test_str_method(self):
        self.assertEqual(str(self.task), "Create API")

    def test_get_absolute_url(self):
        expected_url = reverse(
            "tasks:task-detail", kwargs={"pk": self.task.pk}
        )

        self.assertEqual(self.task.get_absolute_url(), expected_url)
