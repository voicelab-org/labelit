# Generated by Django 3.1.7 on 2022-04-27 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labelit', '0035_auto_20220427_1557'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='description',
            field=models.TextField(null=True, verbose_name='Description of the project'),
        ),
    ]