from django.urls import path

from .views import (
    index,
    TaskListView,
    TaskDetailView,
    TaskUpdateView,
    WorkerListView,
    WorkerDetailView,
    WorkerCreateView,
    WorkerUpdateView,
    TaskTypeListView,
    TaskTypeCreateView,
    TaskTypeUpdateView,
    TaskDeleteView,
    PositionListView,
    PositionCreateView,
    PositionUpdateView,
    TaskCreateView,
)

urlpatterns = [
    path("", index, name="index"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path("tasks/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path("workers/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"),
    path("workers/create/", WorkerCreateView.as_view(), name="worker-create"),
    path("workers/<int:pk>/update/", WorkerUpdateView.as_view(), name="worker-update"),
    path("task-types/", TaskTypeListView.as_view(), name="task-type-list"),
    path("task-types/create/", TaskTypeCreateView.as_view(), name="task-type-create"),
    path(
        "task-types/<int:pk>/update/",
        TaskTypeUpdateView.as_view(),
        name="task-type-update",
    ),
    path("positions/", PositionListView.as_view(), name="position-list"),
    path("positions/create/", PositionCreateView.as_view(), name="position-create"),
    path(
        "positions/<int:pk>/update/",
        PositionUpdateView.as_view(),
        name="position-update",
    ),
]

app_name = "tasks"
