# Generated by Django 3.1.7 on 2022-02-23 11:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("labelit", "0023_auto_20220121_2353"),
    ]

    operations = [
        migrations.AddField(
            model_name="dataset",
            name="is_streamed",
            field=models.BooleanField(default=False),
        ),
    ]
