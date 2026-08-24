from django.contrib import admin
from .models import Position, Worker, TaskType, Task
from django.contrib.auth.admin import UserAdmin


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = ["username", "first_name", "last_name", "email", "position"]
    fieldsets = UserAdmin.fieldsets + (("Additional info", {"fields": ("position",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional info", {"fields": ("position",)}),
    )


admin.site.register(Position)
admin.site.register(TaskType)
admin.site.register(Task)
