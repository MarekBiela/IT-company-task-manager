from django.shortcuts import render
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Task, Worker, TaskType, Position


@login_required
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


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task

    def get_queryset(self):
        queryset = Task.objects.select_related("task_type")
        return queryset


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    queryset = Task.objects.prefetch_related("assignees__position")


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker

    def get_queryset(self):
        queryset = Worker.objects.select_related("position")
        return queryset


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
    queryset = Worker.objects.prefetch_related("tasks__task_type")


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    template_name = "tasks/task_type_list.html"
    context_object_name = "task_type_list"


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
