# Generated by Django 3.1.7 on 2021-03-29 12:01

from django.db import migrations, models
import django.db.models.deletion
import labelit.utils.color_generator


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="Annotation",
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
                (
                    "is_done",
                    models.BooleanField(
                        default=False, verbose_name="If true, annotation is confirmed"
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="Batch",
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
                (
                    "name",
                    models.CharField(
                        max_length=200, verbose_name="The name of the batch"
                    ),
                ),
                (
                    "num_annotators_per_document",
                    models.IntegerField(
                        default=1,
                        verbose_name="The target number of annotators per document",
                    ),
                ),
                (
                    "annotation_mode",
                    models.CharField(
                        choices=[
                            (
                                "all_you_can_annotate",
                                " \n            Annotators can annotate as much they want (up to optional limit)\n            By the end of the batch, annotators may have done unequal amounts\n            of work.\n            ",
                            ),
                            (
                                "even",
                                "\n            By the end of the batch, every annotator will have annotated\n            the same number of documents\n            ",
                            ),
                        ],
                        default="even",
                        max_length=32,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "annotation_limit",
                    models.IntegerField(
                        blank=True,
                        null=True,
                        verbose_name="\n        Maximum number of annotated documents per user in this batch.\n        ",
                    ),
                ),
                (
                    "num_documents",
                    models.IntegerField(
                        default=1,
                        verbose_name="The number of documents in this batch (denormalized field)",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Dataset",
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
                ("name", models.CharField(max_length=200)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="Label",
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
                ("name", models.CharField(blank=True, max_length=200, null=True)),
                (
                    "color",
                    models.CharField(
                        default=labelit.utils.color_generator.random_dark_color,
                        max_length=50,
                        verbose_name="The rbg() color string, e.g. rgb(255,231,78)",
                    ),
                ),
                (
                    "polymorphic_ctype",
                    models.ForeignKey(
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="polymorphic_labelit.label_set+",
                        to="contenttypes.contenttype",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Project",
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
                ("name", models.CharField(max_length=500)),
                ("is_audio_annotated", models.BooleanField(default=True)),
                ("is_text_annotated", models.BooleanField(default=True)),
                (
                    "are_sequences_annotated",
                    models.BooleanField(
                        default=False,
                        verbose_name="\n        If True: documents are presented as entire sequences with order preserved.\n        If False: documents are presented one by one, in no particular order\n        ",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Task",
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
                ("name", models.CharField(max_length=200)),
                (
                    "can_documents_be_invalidated",
                    models.BooleanField(
                        default=True,
                        verbose_name="\n        If true, annotators can tag a document as \"invalid'\n        and skip annotation.\n        ",
                    ),
                ),
                (
                    "image",
                    models.ImageField(blank=True, null=True, upload_to="task-images"),
                ),
                (
                    "polymorphic_ctype",
                    models.ForeignKey(
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="polymorphic_labelit.task_set+",
                        to="contenttypes.contenttype",
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tasks",
                        to="labelit.project",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CategoricalTask",
            fields=[
                (
                    "task_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="labelit.task",
                    ),
                ),
                (
                    "are_categories_exclusive",
                    models.BooleanField(
                        default=True,
                        verbose_name="\n        If true, the annotator cannot select more than one category\n        for the document.\n        ",
                    ),
                ),
            ],
            bases=("labelit.task",),
        ),
        migrations.CreateModel(
            name="OrdinalLabel",
            fields=[
                (
                    "label_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="labelit.label",
                    ),
                ),
                (
                    "index",
                    models.IntegerField(
                        default=0,
                        verbose_name="the index of this label in the ordinal scale",
                    ),
                ),
            ],
            bases=("labelit.label",),
        ),
        migrations.CreateModel(
            name="OrdinalTask",
            fields=[
                (
                    "task_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="labelit.task",
                    ),
                ),
            ],
            bases=("labelit.task",),
        ),
        migrations.CreateModel(
            name="SequenceBatch",
            fields=[
                (
                    "batch_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="labelit.batch",
                    ),
                ),
                (
                    "num_sequences",
                    models.IntegerField(
                        default=1,
                        verbose_name="The number of document sequences in this batch (denormalized field)",
                    ),
                ),
            ],
            bases=("labelit.batch",),
        ),
        migrations.AddField(
            model_name="label",
            name="task",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="labels",
                to="labelit.task",
            ),
        ),
        migrations.CreateModel(
            name="DocumentSequence",
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
                ("name", models.CharField(max_length=300, null=True)),
                (
                    "num_documents",
                    models.IntegerField(
                        default=0,
                        verbose_name="number of documents in sequence (denormalized)",
                    ),
                ),
                (
                    "dataset",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="document_sequences",
                        to="labelit.dataset",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Document",
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
                (
                    "text",
                    models.CharField(
                        blank=True,
                        max_length=100000,
                        null=True,
                        verbose_name="The text content of this document",
                    ),
                ),
                (
                    "audio_filename",
                    models.CharField(
                        blank=True,
                        default=None,
                        max_length=3000,
                        null=True,
                        verbose_name="The audio file name",
                    ),
                ),
                (
                    "sequence_index",
                    models.IntegerField(
                        blank=True,
                        null=True,
                        verbose_name="Index (order) of document in sequence",
                    ),
                ),
                (
                    "dataset",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="documents",
                        to="labelit.dataset",
                    ),
                ),
                (
                    "document_sequence",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="labelit.documentsequence",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="BatchDocumentSequence",
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
                (
                    "num_done_annotators",
                    models.IntegerField(
                        default=0,
                        verbose_name="\n        Number of annotation sets completed by annotators.\n        An annotation set is complete when exactly one annotation by the annotator exists\n        for each task in the project for every document for the unit.\n        For a Batch, the unit is the document itself.\n        For a SequenBatch, the unit is the document sequence.\n        ",
                    ),
                ),
                (
                    "num_annotators",
                    models.IntegerField(
                        default=0,
                        verbose_name="\n        Number of annotators who have annotated or are currently annotating\n        the unit\n        ",
                    ),
                ),
                (
                    "document_sequence",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="labelit.documentsequence",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="BatchDocument",
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
                (
                    "num_done_annotators",
                    models.IntegerField(
                        default=0,
                        verbose_name="\n        Number of annotation sets completed by annotators.\n        An annotation set is complete when exactly one annotation by the annotator exists\n        for each task in the project for every document for the unit.\n        For a Batch, the unit is the document itself.\n        For a SequenBatch, the unit is the document sequence.\n        ",
                    ),
                ),
                (
                    "num_annotators",
                    models.IntegerField(
                        default=0,
                        verbose_name="\n        Number of annotators who have annotated or are currently annotating\n        the unit\n        ",
                    ),
                ),
                (
                    "batch",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="labelit.batch"
                    ),
                ),
                (
                    "document",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="labelit.document",
                    ),
                ),
            ],
        ),
    ]
