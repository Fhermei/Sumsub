from django.http import JsonResponse
from django.shortcuts import render
from .models import SumsubApplicant, SumsubDocument
from django.conf import settings
import requests
from django.core.files.storage import FileSystemStorage


def index(request):
    return render(request, 'index.html')

def create_applicant(request):
    if request.method == 'POST':
        url = f"{settings.SUMSUB_BASE_URL}/resources/applicants"
        headers = {
            "X-App-Token": settings.SUMSUB_APP_TOKEN
        }
        response = requests.post(url, headers=headers)
        if response.status_code == 200:
            response_data = response.json()
            applicant = SumsubApplicant.objects.create(
                applicant_id=response_data['id'],
                status=response_data['status']
            )
            return JsonResponse({"status": "Applicant created successfully", "applicant_id": applicant.applicant_id})
        else:
            return JsonResponse({"error": response.json()}, status=response.status_code)

    return render(request, 'create_applicant.html')

def add_document(request):
    if request.method == 'POST' and request.FILES['document']:
        document = request.FILES['document']
        fs = FileSystemStorage()
        filename = fs.save(document.name, document)
        document_path = fs.path(filename)

        applicant_id = "applicant_id"
        url = f"{settings.SUMSUB_BASE_URL}/resources/applicants/{applicant_id}/info/idDoc"
        headers = {
            "X-App-Token": settings.SUMSUB_APP_TOKEN
        }
        files = {'file': open(document_path, 'rb')}

        response = requests.post(url, files=files, headers=headers)
        if response.status_code == 200:
            response_data = response.json()
            document = SumsubDocument.objects.create(
                applicant_id=applicant_id,
                file_url=response_data['url'],
                status=response_data['status']
            )
            return JsonResponse({"status": "Document added", "document_id": document.id})
        else:
            return JsonResponse({"error": response.json()}, status=response.status_code)

    return render(request, 'add_document.html')

def check_verification(request):
    applicant_id = "applicant_id"
    url = f"{settings.SUMSUB_BASE_URL}/resources/applicants/{applicant_id}/verificationStatus"
    headers = {
        "X-App-Token": settings.SUMSUB_APP_TOKEN
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        verification_status = response.json()
        return JsonResponse({"status": verification_status})
    else:
        return JsonResponse({"error": response.json()}, status=response.status_code)
