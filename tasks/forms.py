from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth import get_user_model

from tasks.models import Task


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
