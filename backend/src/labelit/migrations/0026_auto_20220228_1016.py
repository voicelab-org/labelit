# Generated by Django 3.1.7 on 2022-02-28 10:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("labelit", "0025_auto_20220221_1344"),
    ]

    operations = [
        migrations.AlterField(
            model_name="entitylabel",
            name="end_offset",
            field=models.IntegerField(
                default=0, verbose_name="end offset of the entity in the document text"
            ),
        ),
        migrations.AlterField(
            model_name="entitylabel",
            name="start_offset",
            field=models.IntegerField(
                default=0,
                verbose_name="start offset of the entity in the document text",
            ),
        ),
    ]
