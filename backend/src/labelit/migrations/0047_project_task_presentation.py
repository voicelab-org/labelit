# Generated by Django 4.1.7 on 2023-04-07 16:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("labelit", "0046_projecttask_alter_project_tasks"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="task_presentation",
            field=models.CharField(
                choices=[("list", "list"), ("sequence", "sequence")],
                default="list",
                max_length=3000,
                verbose_name="Configures how tasks are presented to annotators - as a list containing a task, in sequence, etc.",
            ),
        ),
    ]
