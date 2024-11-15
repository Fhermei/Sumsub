from django.db import models

class SumsubApplicant(models.Model):
    external_user_id = models.CharField(max_length=100, unique=True)
    applicant_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"Applicant {self.external_user_id}"

class SumsubDocument(models.Model):
    applicant = models.ForeignKey(SumsubApplicant, on_delete=models.CASCADE)
    document_id = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"Document {self.document_id} for Applicant {self.applicant.external_user_id}"
