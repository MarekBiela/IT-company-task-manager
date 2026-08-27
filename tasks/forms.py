from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from tasks.models import Task, Worker


class TaskForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    deadline = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"})
    )

    class Meta:
        model = Task
        fields = "__all__"

    def clean_deadline(self):
        return clean_deadline(self.cleaned_data["deadline"])


def clean_deadline(deadline):
    if deadline < timezone.now():
        raise ValidationError("The time cannot be in the past.")
    return deadline


class WorkerCreationForm(UserCreationForm):
    username = forms.CharField(help_text="")

    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = UserCreationForm.Meta.fields + (
            "position",
            "first_name",
            "last_name",
            "email",
        )


class PositionUpdateForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ["position"]
