from nltk.metrics.agreement import AnnotationTask


class OrdinalAlphaMetric:
    def __init__(self, num_labels=None):
        self.num_labels = num_labels

    def format_annotations_queryset(self, annotations):
        """
        Returns a list of tuples (annotator_id, document_id, label value).
        All annotations must be completed (is_done=True), and there must be an
        equal number of annotations per document, equal to the number of annotators.

        Parameters:
            annotations (django.db.models.query.QuerySet): the queryset containing all annotations

        Returns
            formatted_annotations ([()]): list of tuples (annotator_id, document_id, label value)
        """
        return annotations.values_list(
            "annotator_id",
            "document_id",
            "labels",
        )

    def ordinal_distance(self, l1, l2):
        """
        Returns the sum of two decimal numbers in binary digits.

        Parameters:
                l1 (int): the first ordinal label
                l2 (int): the second ordinal label

        Returns:
                ordinal_distance (float): The distance, between 0.0 and 1.0
        """
        return abs(l2 - l1) / (self.num_labels - 1)

    def ordinal_krippendorff_alpha(
        self, data=[("c1", "1", 1), ("c2", "1", 1), ("c3", "1", 2)]
    ):
        """
        Returns Krippendorff's alpha for the annotated set

        Parameters:
                data ([tuple]): 2-D dataset, each row represents an annotation.
                                Annotators are called coders.
                                Each tuple represents: (coder, annotated_item, value)

        Returns:
                krippendorff_alpha (float): Krippendorff's alpha
        """
        return AnnotationTask(data=data, distance=self.ordinal_distance).alpha()
