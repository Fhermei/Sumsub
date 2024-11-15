from django.contrib import admin
from .models import SumsubApplicant, SumsubDocument

@admin.register(SumsubApplicant)
class SumsubApplicantAdmin(admin.ModelAdmin):
    list_display = ('external_user_id', 'applicant_id', 'status')
    search_fields = ('external_user_id', 'applicant_id')
    list_filter = ('status',)

@admin.register(SumsubDocument)
class SumsubDocumentAdmin(admin.ModelAdmin):
    list_display = ('applicant', 'document_id')
    search_fields = ('document_id',)
    list_filter = ('applicant',)
