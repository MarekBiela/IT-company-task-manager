from django.shortcuts import render
from django.views import generic

from .models import Task, Worker, TaskType, Position


def index(request):
    num_tasks = Task.objects.count()
    num_workers = Worker.objects.count()
    num_task_types = TaskType.objects.count()
    num_positions = Position.objects.count()

    num_visits = request.session.get("num_visits", 0)
    num_visits += 1
    request.session["num_visits"] = num_visits

    context = {
        "num_tasks": num_tasks,
        "num_workers": num_workers,
        "num_task_types": num_task_types,
        "num_positions": num_positions,
        "num_visits": num_visits,
    }

    return render(request, "tasks/index.html", context=context)


class TaskListView(generic.ListView):
    model = Task

    def get_queryset(self):
        queryset = Task.objects.select_related("task_type")
        return queryset


class WorkerListView(generic.ListView):
    model = Worker

    def get_queryset(self):
        queryset = Worker.objects.select_related("position")
        return queryset


class TaskTypeListView(generic.ListView):
    model = TaskType
    template_name = "tasks/task_type_list.html"
    context_object_name = "task_type_list"


class PositionListView(generic.ListView):
    model = Position
