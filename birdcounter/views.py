from django.shortcuts import render, redirect, get_object_or_404
import boto3
import io
import uuid
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from botocore.exceptions import ClientError
from django.conf import settings
from botocore.client import Config
from PyPDF2 import PdfReader
import pytesseract
from PIL import Image
from django.shortcuts import render
from django.conf import settings
from .models import PDFDocument
from pdf2image import convert_from_path
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import uuid
from datetime import datetime
from .models import PDFDocument, BirdCount



# Create your views here.

def home(request):
    if request.user.is_authenticated:
        documents = PDFDocument.objects.filter(user=request.user)
        if documents.exists():
            return render(request, 'home.html', {'documents': documents})
        else:
            return render(request, 'home.html', {'show_upload_prompt': True})
    else:
        return render(request, 'home.html')
    

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Redirect to home page after successful signup
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})



@login_required
def document_list(request):
    documents = PDFDocument.objects.filter(user=request.user).order_by('-uploaded_at')
    return render(request, 'document_list.html', {'documents': documents})

@login_required
def document_detail(request, document_id):
    document = PDFDocument.objects.get(id=document_id, user=request.user)
    bird_counts = BirdCount.objects.filter(document=document)
    return render(request, 'document_detail.html', {'document': document, 'bird_counts': bird_counts})


@login_required
def document_detail(request, document_id):
    document = get_object_or_404(PDFDocument, id=document_id, user=request.user)
    bird_counts = BirdCount.objects.filter(document=document).values('bird_name', 'count')
    
    # Convert QuerySet to dictionary for easier template rendering
    bird_counts_dict = {item['bird_name']: item['count'] for item in bird_counts}
    
    return render(request, 'document_detail.html', {
        'document': document,
        'bird_counts': bird_counts_dict
    })


def convert_pdf_to_image(pdf_path, page_number):
    images = convert_from_path(pdf_path, first_page=page_number, last_page=page_number)
    return images[0]


@login_required
def upload_and_count_birds(request):
    if request.method == 'POST' and request.FILES['pdf_file']:
        pdf_file = request.FILES['pdf_file']

        # Generate a unique file name
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        file_name = f'pdfs/{request.user.username}/{timestamp}_{unique_id}_{pdf_file.name}'

        try:
            file_content = pdf_file.read()

            if settings.ON_RENDER:
                session = boto3.Session(
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                    region_name=settings.AWS_S3_REGION_NAME
                )
                s3 = session.client('s3', config=Config(signature_version='s3v4'),
                            use_ssl=True, verify=None)
                
                file_obj_upload = io.BytesIO(file_content)
                s3.upload_fileobj(file_obj_upload, settings.AWS_STORAGE_BUCKET_NAME, file_name)
            else:
                default_storage.save(file_name, ContentFile(file_content))

            file_obj_process = io.BytesIO(file_content)
            
        except ClientError as e:
            print(f"An error occurred: {e}")
            return render(request, 'error.html', {'error': 'File upload failed'})
        
        bird_names = ['crow', 'ostrich', 'eagle', 'sparrow', 'penguin']
        bird_counts = {bird: 0 for bird in bird_names}
        
        try:
            pdf_reader = PdfReader(file_obj_process)
   
            for page in pdf_reader.pages:
                text = page.extract_text()
                if not text:
                    image = convert_pdf_to_image(page)
                    text = pytesseract.image_to_string(image)
                
                for bird in bird_names:
                    bird_counts[bird] += text.lower().count(bird)
            
            # Save the document and bird counts
            document = PDFDocument.objects.create(
                user=request.user,
                file=file_name,
                title=pdf_file.name
            )
            for bird, count in bird_counts.items():
                BirdCount.objects.create(document=document, bird_name=bird, count=count)
            
        except ClientError as e:
            print(f"An error occurred: {e}")
            return render(request, 'error.html', {'error': 'File processing failed'})
        
        return redirect('document_detail', document_id=document.id)
    
    return render(request, 'upload.html')






def convert_pdf_to_image(pdf_path, page_number):
    images = convert_from_path(pdf_path, first_page=page_number, last_page=page_number)
    return images[0]





