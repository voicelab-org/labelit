# Generated by Django 4.1.7 on 2023-04-16 19:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("labelit", "0049_document_video_filename_project_is_video_annotated"),
    ]

    operations = [
        migrations.CreateModel(
            name="EmotionCategoricalLabel",
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
                    "tags_with_intensities",
                    models.JSONField(
                        verbose_name="The collection of <tag, intensity> pairs"
                    ),
                ),
            ],
            bases=("labelit.label",),
        ),
        migrations.CreateModel(
            name="EmotionCategoricalTask",
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
