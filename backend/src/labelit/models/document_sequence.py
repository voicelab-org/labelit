from django.db import models


class DocumentSequence(models.Model):
    name = models.CharField(max_length=300, null=True)
    dataset = models.ForeignKey(
        "labelit.Dataset", on_delete=models.CASCADE, related_name="document_sequences"
    )
    # BEGIN denormalized fields
    num_documents = models.IntegerField(
        "number of documents in sequence (denormalized)", default=0
    )
    # END denormalized fields
