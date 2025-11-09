"""
File processing utilities
Handles extraction of text from various file formats
"""
import io
import logging
import PyPDF2
from docx import Document

logger = logging.getLogger(__name__)

def extract_text_from_file(file):
    """
    Extract text from uploaded files with better error handling
    
    Args:
        file: File object from Flask request
        
    Returns:
        str: Extracted text content
        
    Raises:
        ValueError: If file format is unsupported
        Exception: If extraction fails
    """
    try:
        filename = file.filename.lower()
        
        if filename.endswith('.txt'):
            return file.read().decode('utf-8')
            
        elif filename.endswith('.pdf'):
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
            
        elif filename.endswith(('.doc', '.docx')):
            doc = Document(io.BytesIO(file.read()))
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
            
        else:
            raise ValueError("Unsupported file format")
            
    except ValueError as e:
        logger.error(f"Unsupported file format: {e}")
        raise
    except Exception as e:
        logger.error(f"File extraction error: {e}")
        raise Exception(f"Failed to extract text from file: {e}")

