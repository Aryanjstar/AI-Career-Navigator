"""
File processing utilities for resume upload
"""
import io
import logging
from typing import BinaryIO
import PyPDF2
from docx import Document

logger = logging.getLogger(__name__)


def extract_text_from_file(file: BinaryIO) -> str:
    """
    Extract text from uploaded files (PDF, DOC, DOCX, TXT)
    
    Args:
        file: File object from Flask request
        
    Returns:
        Extracted text content
        
    Raises:
        ValueError: If file format is not supported
        Exception: If text extraction fails
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
            raise ValueError("Unsupported file format. Supported formats: TXT, PDF, DOC, DOCX")
            
    except Exception as e:
        logger.error(f"File extraction error: {e}")
        raise Exception(f"Failed to extract text from file: {e}")

