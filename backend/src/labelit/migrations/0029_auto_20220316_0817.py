# Generated by Django 3.1.7 on 2022-03-16 08:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("labelit", "0028_auto_20220316_0813"),
    ]

    operations = [
        migrations.AddField(
            model_name="batch",
            name="archived",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="project",
            name="archived",
            field=models.BooleanField(default=False),
        ),
    ]
