# Generated by Django 3.1.7 on 2021-07-10 21:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("labelit", "0004_auto_20210709_0902"),
    ]

    operations = [
        migrations.AddField(
            model_name="annotation",
            name="time",
            field=models.IntegerField(
                default=0,
                verbose_name="The time (ms) taken to annotate the document (possibly including other annotations for other tasks)",
            ),
        ),
        migrations.AlterField(
            model_name="transcriptionlabel",
            name="transcript",
            field=models.TextField(
                blank=True, default="", verbose_name="the transcript"
            ),
        ),
    ]