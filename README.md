# Bird Count PDF Analyzer

## Project Overview

The Bird Count PDF Analyzer is a web application that allows users to upload PDF documents and analyze them for occurrences of bird names. The application provides a user-friendly interface for uploading PDFs, displays the bird count results, 
and maintains a history of uploaded documents.

## Technology Stack

- **Backend**: Django (Python web framework)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite (for development), PostgreSQL (for production)
- **PDF Processing**: PyPDF2 for text extraction
- **OCR (Optical Character Recognition)**: Tesseract OCR via pytesseract
- **Image Processing**: Pillow (PIL) for image manipulation
- **Deployment**: Render (cloud platform)

## Key Features

- User authentication and registration
- PDF upload and processing
- Bird count analysis and result display
- Document history for registered users
- OCR capability for image-based PDFs


### Prerequisites

- Python 3.x
- pip (Python package manager)
- PostgreSQL (for production)
- Amazon S3 Setup and give the credentials in .env file

### Clone the Repository

```bash
git clone https://github.com/yourusername/bird-count-pdf-analyzer.git
cd bird-count-pdf-analyzer
