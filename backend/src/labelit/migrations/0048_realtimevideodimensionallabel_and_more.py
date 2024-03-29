# Generated by Django 4.1.7 on 2023-04-13 15:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("labelit", "0047_project_task_presentation"),
    ]

    operations = [
        migrations.CreateModel(
            name="RealtimeVideoDimensionalLabel",
            fields=[
                (
                    "label_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="labelit.label",
                    ),
                ),
                (
                    "sequence",
                    models.JSONField(
                        verbose_name="The sequence of <video time, dimensional value> pairs"
                    ),
                ),
                (
                    "summative",
                    models.IntegerField(
                        verbose_name="The summative (synthetic) annotation associated with the entire video"
                    ),
                ),
            ],
            bases=("labelit.label",),
        ),
        migrations.CreateModel(
            name="RealtimeVideoDimensionalTask",
            fields=[
                (
                    "task_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="labelit.task",
                    ),
                ),
            ],
            bases=("labelit.task",),
        ),
    ]
