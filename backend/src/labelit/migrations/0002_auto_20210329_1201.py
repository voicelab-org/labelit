# Generated by Django 3.1.7 on 2021-03-29 12:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("labelit", "0001_initial"),
        ("contenttypes", "0002_remove_content_type_name"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="batch",
            name="annotators",
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name="batch",
            name="dataset",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="labelit.dataset"
            ),
        ),
        migrations.AddField(
            model_name="batch",
            name="documents",
            field=models.ManyToManyField(
                related_name="batches",
                through="labelit.BatchDocument",
                to="labelit.Document",
            ),
        ),
        migrations.AddField(
            model_name="batch",
            name="polymorphic_ctype",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="polymorphic_labelit.batch_set+",
                to="contenttypes.contenttype",
            ),
        ),
        migrations.AddField(
            model_name="batch",
            name="project",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="batches",
                to="labelit.project",
            ),
        ),
        migrations.AddField(
            model_name="annotation",
            name="annotator",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="annotation",
            name="batch",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="annotations",
                to="labelit.batch",
            ),
        ),
        migrations.AddField(
            model_name="annotation",
            name="document",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="labelit.document"
            ),
        ),
        migrations.AddField(
            model_name="annotation",
            name="document_sequence",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="labelit.documentsequence",
            ),
        ),
        migrations.AddField(
            model_name="annotation",
            name="labels",
            field=models.ManyToManyField(
                related_name="annotations", to="labelit.Label"
            ),
        ),
        migrations.AddField(
            model_name="annotation",
            name="project",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="labelit.project"
            ),
        ),
        migrations.AddField(
            model_name="annotation",
            name="task",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="labelit.task"
            ),
        ),
        migrations.AddField(
            model_name="sequencebatch",
            name="sequences",
            field=models.ManyToManyField(
                through="labelit.BatchDocumentSequence", to="labelit.DocumentSequence"
            ),
        ),
        migrations.AddField(
            model_name="batchdocumentsequence",
            name="batch",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="labelit.sequencebatch"
            ),
        ),
    ]
