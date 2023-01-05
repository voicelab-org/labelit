from django.db import models


class Lexicon(models.Model):
    name = models.CharField(
        max_length=300,
    )

    tasks = models.ManyToManyField("labelit.Task", related_name="lexicons")

    """
    projects = models.ManyToManyField(
        'labelit.Project',
    )
    """

    class Meta:
        app_label = "labelit"

    def __str__(self):
        return "<Lexicon-{}: {}>".format(self.pk, self.name)
