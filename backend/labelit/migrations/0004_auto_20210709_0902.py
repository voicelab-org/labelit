# Generated by Django 3.1.7 on 2021-07-09 09:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('labelit', '0003_auto_20210707_1249'),
    ]

    operations = [
        migrations.CreateModel(
            name='TranscriptionLabel',
            fields=[
                ('label_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='labelit.label')),
                ('transcript', models.TextField(default=0, verbose_name='the transcript')),
            ],
            bases=('labelit.label',),
        ),
        migrations.CreateModel(
            name='TranscriptionTask',
            fields=[
                ('task_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='labelit.task')),
                ('validator', models.CharField(default='labelit.validators.base_transcription_validator.BaseTranscriptionValidator', max_length=500, verbose_name='Dotted path to the validator class')),
            ],
            bases=('labelit.task',),
        ),
        migrations.AlterField(
            model_name='annotation',
            name='qa_invalidation_comment',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name="The comment accompanying a QA's invalidation"),
        ),
    ]
