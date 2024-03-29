# Generated by Django 3.1.7 on 2021-07-12 09:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("labelit", "0006_auto_20210711_1504"),
    ]

    operations = [
        migrations.CreateModel(
            name="Lexicon",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=300)),
                ("projects", models.ManyToManyField(to="labelit.Project")),
            ],
        ),
        migrations.AlterField(
            model_name="task",
            name="html_guidelines",
            field=models.TextField(blank=True, default="<h2>Customize guidelines</h2>"),
        ),
        migrations.CreateModel(
            name="LexiconEntry",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("entry", models.CharField(max_length=500)),
                (
                    "lexicon",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="entries",
                        to="labelit.lexicon",
                    ),
                ),
            ],
        ),
    ]
