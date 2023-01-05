# Generated by Django 3.1.7 on 2022-10-11 18:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("labelit", "0040_project_created_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="created_by",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="project",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
