# Generated by Django 4.1.7 on 2023-04-13 15:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("labelit", "0048_realtimevideodimensionallabel_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="document",
            name="video_filename",
            field=models.CharField(
                blank=True,
                default=None,
                max_length=3000,
                null=True,
                verbose_name="The video file name",
            ),
        ),
        migrations.AddField(
            model_name="project",
            name="is_video_annotated",
            field=models.BooleanField(default=False),
        ),
    ]