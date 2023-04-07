from django.db import models
from .task import Task
from .project import Project


class ProjectTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    order = models.IntegerField(
        "order in which the task is shown during annotation", default=1
    )
