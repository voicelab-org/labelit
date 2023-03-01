# Generated by Django 3.1.7 on 2021-07-07 12:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("labelit", "0002_auto_20210329_1201"),
    ]

    operations = [
        migrations.AddField(
            model_name="annotation",
            name="has_qa_invalidated",
            field=models.BooleanField(
                default=False,
                verbose_name="Whether QA has marked annotation as invalid",
            ),
        ),
        migrations.AddField(
            model_name="annotation",
            name="has_qa_validated",
            field=models.BooleanField(
                default=False, verbose_name="Whether QA has marked annotation as valid"
            ),
        ),
        migrations.AddField(
            model_name="annotation",
            name="is_resubmitted",
            field=models.BooleanField(
                default=False,
                verbose_name="Whether annotator has resubmitted the annotation following invalidation by QA",
            ),
        ),
        migrations.AddField(
            model_name="annotation",
            name="qa_invalidation_comment",
            field=models.CharField(
                max_length=500,
                null=True,
                verbose_name="The comment accompanying a QA's invalidation",
            ),
        ),
    ]