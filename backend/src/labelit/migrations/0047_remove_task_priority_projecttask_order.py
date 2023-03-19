# Generated by Django 4.1.7 on 2023-03-12 20:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("labelit", "0046_projecttask_alter_project_tasks"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="task",
            name="priority",
        ),
        migrations.AddField(
            model_name="projecttask",
            name="order",
            field=models.IntegerField(
                default=1,
                verbose_name="order in which the task is shown during annotation",
            ),
        ),
    ]