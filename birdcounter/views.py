from django.shortcuts import render
import os
import boto3
import io
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


# Create your views here.
def convert_pdf_to_image(pdf_path, page_number):
    images = convert_from_path(pdf_path, first_page=page_number, last_page=page_number)
    return images[0]


def count_bird_names(request):
    if request.method == 'POST' and request.FILES['pdf_file']:
        pdf_file = request.FILES['pdf_file']

        # Generate a unique file name
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        file_name = f'pdfs/{timestamp}_{unique_id}_{pdf_file.name}'

        try:
            file_content = pdf_file.read()

            if settings.ON_RENDER:
                 # Create a custom session with specific credentials
                session = boto3.Session(
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                    region_name=settings.AWS_S3_REGION_NAME
                )
                # Create S3 client with the custom session and disable credential lookup
                s3 = session.client('s3', config=Config(signature_version='s3v4'),
                            use_ssl=True, verify=None)
                
                # Create a file-like object
                file_obj_upload = io.BytesIO(file_content)
                s3.upload_fileobj(file_obj_upload, settings.AWS_STORAGE_BUCKET_NAME, file_name)
                

            else:
                # Development: Use local storage
                default_storage.save(file_name, ContentFile(file_content))

            # Create a file-like object for processing
            file_obj_process = io.BytesIO(file_content)

            
        except ClientError as e:
            print(f"An error occurred: {e}")
            # Reset file pointer for further processing
            
            return render(request, 'error.html', {'error': 'File upload failed'})
        
        bird_names = ['crow', 'ostrich', 'eagle', 'sparrow', 'penguin']
        bird_counts = {bird: 0 for bird in bird_names}
        
        # Download file from S3 and process
        try:
            pdf_reader = PdfReader(file_obj_process)
   
            for page in pdf_reader.pages:
                text = page.extract_text()
                if not text:
                    # If text extraction fails, use OCR
                    image = convert_pdf_to_image(page)
                    text = pytesseract.image_to_string(image)
                
                for bird in bird_names:
                    bird_counts[bird] += text.lower().count(bird)
            
            # Optionally, delete the file after processing
            # if settings.ON_RENDER:
            #     s3.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=file_name)
            # else:
            #     default_storage.delete(file_name)
            
        except ClientError as e:
            print(f"An error occurred: {e}")
            return render(request, 'error.html', {'error': 'File processing failed'})
        
        return render(request, 'result.html', {'bird_counts': bird_counts})
    
    return render(request, 'upload.html')

