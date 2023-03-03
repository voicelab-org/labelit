from django.contrib import admin

from .models import (
    Project,
    Dataset,
    Document,
    DocumentSequence,
    Batch,
    SequenceBatch,
    Label,
    OrdinalLabel,
    OrdinalTask,
    CategoricalTask,
    BatchDocument,
    BatchDocumentSequence,
    Annotation,
    TranscriptionTask,
    TextEditionTask,
    Lexicon,
    LexiconEntry,
    LiveCorrectLabel,
    LiveCorrectTask,
    NestedCategoricalLabel,
    NestedCategoricalTask,
    TimedTranscript,
    TimedTranscriptSegment,
    EntityLabel,
    EntityTask,
    AudioRegionLabel,
    AudioRegionTask,
)

admin.site.register(Project)

admin.site.register(BatchDocument)
admin.site.register(BatchDocumentSequence)
admin.site.register(Annotation)
admin.site.register(TranscriptionTask)
admin.site.register(TextEditionTask)
admin.site.register(LiveCorrectTask)
admin.site.register(LiveCorrectLabel)
admin.site.register(AudioRegionTask)
admin.site.register(AudioRegionLabel)


class TimedTranscriptSegmentInline(admin.TabularInline):
    model = TimedTranscriptSegment


class TimedTranscriptAdmin(admin.ModelAdmin):
    inlines = [TimedTranscriptSegmentInline]


admin.site.register(TimedTranscript, TimedTranscriptAdmin)


class DocumentSequenceInline(admin.TabularInline):
    model = DocumentSequence


class DocumentInline(admin.TabularInline):
    model = Document


class DatasetAdmin(admin.ModelAdmin):
    inlines = [DocumentInline, DocumentSequenceInline]


admin.site.register(Document)


class DocumentSequenceAdmin(admin.ModelAdmin):
    inlines = [DocumentInline]


admin.site.register(DocumentSequence, DocumentSequenceAdmin)
admin.site.register(Dataset, DatasetAdmin)


class LexiconEntryInline(admin.TabularInline):
    model = LexiconEntry


class LexiconAdmin(admin.ModelAdmin):
    inlines = [LexiconEntryInline]


admin.site.register(Lexicon, LexiconAdmin)


class LabelInline(admin.TabularInline):
    model = Label


class CategoricalTaskAdmin(admin.ModelAdmin):
    inlines = [LabelInline]


admin.site.register(Label)
admin.site.register(CategoricalTask, CategoricalTaskAdmin)
admin.site.register(NestedCategoricalTask)


class NestedCategoricalLabelInline(admin.TabularInline):
    model = NestedCategoricalLabel
    fk_name = "parent_label"


class NestedCategoricalLabelAdmin(admin.ModelAdmin):
    inlines = [NestedCategoricalLabelInline]


admin.site.register(NestedCategoricalLabel, NestedCategoricalLabelAdmin)


class OrdinalLabelInline(admin.TabularInline):
    model = OrdinalLabel


admin.site.register(OrdinalLabel)


class OrdinalTaskAdmin(admin.ModelAdmin):
    inlines = [OrdinalLabelInline]


class EntityLabelInline(admin.TabularInline):
    model = EntityLabel


class EntityTaskAdmin(admin.ModelAdmin):
    inlines = [EntityLabelInline]


admin.site.register(EntityTask, EntityTaskAdmin)


admin.site.register(OrdinalTask, OrdinalTaskAdmin)


class BatchDocumentInline(admin.TabularInline):
    model = Batch.documents.through


class BatchAdmin(admin.ModelAdmin):
    inlines = [
        BatchDocumentInline,
    ]


admin.site.register(Batch, BatchAdmin)


class BatchDocumentSequenceInline(admin.TabularInline):
    model = SequenceBatch.sequences.through


class SequenceBatchAdmin(admin.ModelAdmin):
    inlines = [
        BatchDocumentSequenceInline,
    ]


admin.site.register(SequenceBatch, SequenceBatchAdmin)
