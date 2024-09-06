from django.shortcuts import render
import os
from PyPDF2 import PdfReader
import pytesseract
from PIL import Image
from django.shortcuts import render
from django.conf import settings
from .models import PDFDocument
from pdf2image import convert_from_path

def convert_pdf_to_image(pdf_path, page_number):
    images = convert_from_path(pdf_path, first_page=page_number, last_page=page_number)
    return images[0]

# Create your views here.

def count_bird_names(request):
    if request.method == 'POST' and request.FILES['pdf_file']:
        pdf_file = request.FILES['pdf_file']
        document = PDFDocument.objects.create(file=pdf_file)
        bird_names = ['crow','ostrich','eagle','sparrow','penguin']
        bird_counts = {bird : 0 for bird in bird_names}
        pdf_path = os.path.join(settings.MEDIA_ROOT, str(document.file))

        with open(pdf_path, 'rb') as f:
            pdf_reader = PdfReader(f)
            for page in pdf_reader.pages:
                text = page.extract_text()
                if not text:

                    # if text extraction fails, use OCR
                    image = convert_pdf_to_image(page)
                    text = pytesseract.image_to_string(image)

                for bird in bird_names:
                    bird_counts[bird] += text.lower().count(bird)

        return render(request, 'result.html',{'bird_counts': bird_counts})

    return render(request, 'upload.html')

def convert_pdf_to_image(page):
    # This function needs to be implemented
    # You might use a library like pdf2image for this purpose
    pass
