# Generated by Django 3.1.7 on 2022-04-05 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labelit', '0032_texteditionlabel_texteditiontask'),
    ]

    operations = [
        migrations.AddField(
            model_name='texteditiontask',
            name='validator',
            field=models.CharField(default='labelit.validators.base_transcription_validator.BaseTranscriptionValidator', max_length=500, verbose_name='Dotted path to the validator class'),
        ),
    ]