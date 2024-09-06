from django.db import models

# Create your models here.

class PDFDocument(models.Model):
    file = models.FileField(upload_to='pdfs')
    upload_at = models.DateTimeField(auto_now_add=True)
    
