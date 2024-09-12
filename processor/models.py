from django.db import models


class PDFData(models.Model):
    email = models.EmailField(unique=True)
    nouns = models.JSONField()
    verbs = models.JSONField()

    def __str__(self):
        return self.email
