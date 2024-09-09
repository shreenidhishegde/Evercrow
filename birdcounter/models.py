from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# class PDFDocument(models.Model):
#     file = models.FileField(upload_to='pdfs')
#     upload_at = models.DateTimeField(auto_now_add=True)
    
class PDFDocument(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pdf_documents')
    file = models.FileField(upload_to='pdfs')
    title = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.user.username if self.user else 'No User'}"

class BirdCount(models.Model):
    document = models.ForeignKey(PDFDocument, on_delete=models.CASCADE, related_name='bird_counts')
    bird_name = models.CharField(max_length=100)
    count = models.IntegerField()

    def __str__(self):
        return f"{self.bird_name}: {self.count} in {self.document.title or 'Untitled'}"