# Generated by Django 3.1.7 on 2021-07-27 09:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("labelit", "0014_auto_20210726_0934"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="livecorrectlabel",
            name="timed_transcript_segment",
        ),
        migrations.RemoveField(
            model_name="livecorrectlabel",
            name="transcript",
        ),
        migrations.AddField(
            model_name="livecorrectlabel",
            name="timed_transcript",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="labelit.timedtranscript",
            ),
        ),
    ]
