from django.urls import path

from .views import index, WorkerListView, TaskListView, TaskTypeListView

urlpatterns = [
    path("", index, name="index"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path("task-types/", TaskTypeListView.as_view(), name="task-type-list"),
]

app_name = "tasks"
