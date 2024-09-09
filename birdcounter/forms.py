from django import forms
from .models import PDFDocument

class PDFDocumentForm(forms.ModelForm):
    class Meta:
        model = PDFDocument
        fields = ['file', 'title']
        widgets = {
            'file': forms.FileInput(attrs={'accept': '.pdf'}),
            'title': forms.TextInput(attrs={'placeholder': 'Enter document title (optional)'}),
        }