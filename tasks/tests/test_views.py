from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from tasks.models import Position, Task, TaskType, Worker


class BaseViewTest(TestCase):

    def setUp(self):
        self.position = Position.objects.create(name="Developer")

        self.worker = Worker.objects.create_user(
            username="john",
            password="test12345",
            first_name="John",
            last_name="Smith",
            position=self.position,
        )

        self.task_type = TaskType.objects.create(name="Development")

        self.task = Task.objects.create(
            name="Create API",
            description="Develop a REST API",
            deadline=timezone.now() + timedelta(days=7),
            priority="3",
            task_type=self.task_type,
        )

        self.client.force_login(self.worker)


class IndexViewTest(BaseViewTest):

    def test_index_view(self):
        response = self.client.get(reverse("tasks:index"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/index.html")

        self.assertEqual(response.context["num_tasks"], 1)
        self.assertEqual(response.context["num_workers"], 1)
        self.assertEqual(response.context["num_task_types"], 1)
        self.assertEqual(response.context["num_positions"], 1)

    def test_num_visits_increments(self):
        url = reverse("tasks:index")

        self.client.get(url)
        response = self.client.get(url)

        self.assertEqual(response.context["num_visits"], 2)


class TaskViewTest(BaseViewTest):

    def test_task_list_view(self):
        response = self.client.get(reverse("tasks:task-list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create API")

    def test_task_search(self):
        response = self.client.get(
            reverse("tasks:task-list"),
            {"name": "API"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create API")

    def test_task_search_no_results(self):
        response = self.client.get(
            reverse("tasks:task-list"),
            {"name": "Nonexistent"},
        )

        self.assertEqual(len(response.context["task_list"]), 0)

    def test_task_pagination(self):
        for i in range(6):
            Task.objects.create(
                name=f"Task {i}",
                description="Description",
                deadline=timezone.now() + timedelta(days=7),
                priority="3",
                task_type=self.task_type,
            )

        response = self.client.get(reverse("tasks:task-list"))
        self.assertEqual(len(response.context["task_list"]), 5)

        response = self.client.get(
            reverse("tasks:task-list"),
            {"page": 2},
        )
        self.assertEqual(len(response.context["task_list"]), 2)

    def test_task_detail_view(self):
        response = self.client.get(
            reverse("tasks:task-detail", kwargs={"pk": self.task.pk})
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create API")

    def test_task_create_view(self):
        data = {
            "name": "New API",
            "description": "Create a new REST API",
            "deadline": (timezone.now() + timedelta(days=10)).date(),
            "priority": "2",
            "task_type": self.task_type.pk,
            "assignees": [self.worker.pk],
        }

        response = self.client.post(
            reverse("tasks:task-create"),
            data,
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(name="New API").exists())

    def test_task_update_view(self):
        response = self.client.post(
            reverse("tasks:task-update", kwargs={"pk": self.task.pk}),
            {
                "name": "Updated API",
                "description": self.task.description,
                "deadline": self.task.deadline,
                "priority": self.task.priority,
                "task_type": self.task.task_type.pk,
                "assignees": [self.worker.pk],
            },
        )

        self.assertEqual(response.status_code, 302)

        self.task.refresh_from_db()
        self.assertEqual(self.task.name, "Updated API")

    def test_task_delete_view(self):
        response = self.client.post(
            reverse("tasks:task-delete", kwargs={"pk": self.task.pk})
        )

        self.assertRedirects(response, reverse("tasks:task-list"))
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())

    def test_toggle_assign_to_task(self):
        url = reverse(
            "tasks:toggle-task-assign",
            kwargs={"pk": self.task.pk},
        )

        detail_url = reverse(
            "tasks:task-detail",
            kwargs={"pk": self.task.pk},
        )

        response = self.client.get(url)

        self.assertRedirects(response, detail_url)
        self.assertIn(self.worker, self.task.assignees.all())

        response = self.client.get(url)

        self.assertRedirects(response, detail_url)
        self.assertNotIn(self.worker, self.task.assignees.all())


class WorkerViewTest(BaseViewTest):

    def test_worker_list_view(self):
        response = self.client.get(reverse("tasks:worker-list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "john")

    def test_worker_search(self):
        response = self.client.get(
            reverse("tasks:worker-list"),
            {"username": "john"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "john")

    def test_worker_search_no_results(self):
        response = self.client.get(
            reverse("tasks:worker-list"),
            {"username": "nonexistent"},
        )

        self.assertEqual(len(response.context["worker_list"]), 0)

    def test_worker_pagination(self):
        for i in range(7):
            Worker.objects.create_user(
                username=f"worker{i}",
                password="test12345",
                position=self.position,
            )

        response = self.client.get(reverse("tasks:worker-list"))
        self.assertEqual(len(response.context["worker_list"]), 5)

        response = self.client.get(
            reverse("tasks:worker-list"),
            {"page": 2},
        )
        self.assertEqual(len(response.context["worker_list"]), 3)

    def test_worker_detail_view(self):
        response = self.client.get(
            reverse("tasks:worker-detail", kwargs={"pk": self.worker.pk})
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "john")

    def test_worker_create_view(self):
        data = {
            "username": "michael",
            "password1": "StrongPassword123!",
            "password2": "StrongPassword123!",
            "first_name": "Michael",
            "last_name": "Brown",
            "position": self.position.pk,
        }

        response = self.client.post(
            reverse("tasks:worker-create"),
            data,
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Worker.objects.filter(username="michael").exists())

    def test_worker_update_view(self):
        new_position = Position.objects.create(name="Manager")

        response = self.client.post(
            reverse("tasks:worker-update", kwargs={"pk": self.worker.pk}),
            {"position": new_position.pk},
        )

        self.assertEqual(response.status_code, 302)

        self.worker.refresh_from_db()
        self.assertEqual(self.worker.position, new_position)

    def test_worker_delete_view(self):
        response = self.client.post(
            reverse("tasks:worker-delete", kwargs={"pk": self.worker.pk})
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("tasks:worker-list"))
        self.assertFalse(Worker.objects.filter(pk=self.worker.pk).exists())


class TaskTypeViewTest(BaseViewTest):

    def test_task_type_list_view(self):
        response = self.client.get(reverse("tasks:task-type-list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Development")

    def test_task_type_search(self):
        response = self.client.get(
            reverse("tasks:task-type-list"),
            {"name": "Development"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Development")

    def test_task_type_search_no_results(self):
        response = self.client.get(
            reverse("tasks:task-type-list"),
            {"name": "Nonexistent"},
        )

        self.assertEqual(len(response.context["task_type_list"]), 0)

    def test_task_type_pagination(self):
        for i in range(8):
            TaskType.objects.create(name=f"Type {i}")

        response = self.client.get(reverse("tasks:task-type-list"))
        self.assertEqual(len(response.context["task_type_list"]), 5)

        response = self.client.get(
            reverse("tasks:task-type-list"),
            {"page": 2},
        )
        self.assertEqual(len(response.context["task_type_list"]), 4)

    def test_task_type_create_view(self):
        response = self.client.post(
            reverse("tasks:task-type-create"),
            {"name": "Testing"},
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(TaskType.objects.filter(name="Testing").exists())

    def test_task_type_update_view(self):
        response = self.client.post(
            reverse(
                "tasks:task-type-update",
                kwargs={"pk": self.task_type.pk},
            ),
            {"name": "Testing"},
        )

        self.assertEqual(response.status_code, 302)

        self.task_type.refresh_from_db()
        self.assertEqual(self.task_type.name, "Testing")

    def test_task_type_delete_view(self):
        self.task.delete()

        response = self.client.post(
            reverse(
                "tasks:task-type-delete",
                kwargs={"pk": self.task_type.pk},
            )
        )

        self.assertRedirects(
            response,
            reverse("tasks:task-type-list"),
        )

        self.assertFalse(
            TaskType.objects.filter(pk=self.task_type.pk).exists()
        )


class PositionViewTest(BaseViewTest):

    def test_position_list_view(self):
        response = self.client.get(reverse("tasks:position-list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Developer")

    def test_position_search(self):
        response = self.client.get(
            reverse("tasks:position-list"),
            {"name": "Developer"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Developer")

    def test_position_search_no_results(self):
        response = self.client.get(
            reverse("tasks:position-list"),
            {"name": "Nonexistent"},
        )

        self.assertEqual(len(response.context["position_list"]), 0)

    def test_position_pagination(self):
        for i in range(11):
            Position.objects.create(name=f"Position {i}")

        response = self.client.get(reverse("tasks:position-list"))
        self.assertEqual(len(response.context["position_list"]), 5)

        response = self.client.get(
            reverse("tasks:position-list"),
            {"page": 2},
        )
        self.assertEqual(len(response.context["position_list"]), 5)

    def test_position_create_view(self):
        response = self.client.post(
            reverse("tasks:position-create"),
            {"name": "Manager"},
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Position.objects.filter(name="Manager").exists())

    def test_position_update_view(self):
        response = self.client.post(
            reverse(
                "tasks:position-update",
                kwargs={"pk": self.position.pk},
            ),
            {"name": "Manager"},
        )

        self.assertEqual(response.status_code, 302)

        self.position.refresh_from_db()
        self.assertEqual(self.position.name, "Manager")

    def test_position_delete_view(self):
        position = Position.objects.create(name="Manager")

        response = self.client.post(
            reverse(
                "tasks:position-delete",
                kwargs={"pk": position.pk},
            )
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse("tasks:position-list"),
        )

        self.assertFalse(Position.objects.filter(pk=position.pk).exists())


class LoginRequiredTest(TestCase):

    def test_index_requires_login(self):
        response = self.client.get(reverse("tasks:index"))
        self.assertEqual(response.status_code, 302)

    def test_task_list_requires_login(self):
        response = self.client.get(reverse("tasks:task-list"))
        self.assertEqual(response.status_code, 302)
