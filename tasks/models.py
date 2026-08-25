from django.db import models
from django.contrib.auth.models import AbstractUser


class Position(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.PROTECT,
        related_name="workers",
    )

    class Meta:
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"


class TaskType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    deadline = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        choices=[
            ("4", "Urgent"),
            ("3", "High"),
            ("2", "Medium"),
            ("1", "Low"),
        ],
    )
    task_type = models.ForeignKey(
        TaskType,
        on_delete=models.PROTECT,
        related_name="tasks",
    )
    assignees = models.ManyToManyField(Worker, related_name="tasks")

    class Meta:
        ordering = ["is_completed", "deadline", "-priority"]

    def __str__(self):
        return f"{self.name}"
