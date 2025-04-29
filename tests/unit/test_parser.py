"""
Test script to verify the email parser functionality with sample PDFs.
"""
import os
import sys
import subprocess
from pathlib import Path

sys.path.append(os.path.join(os.path.dirname(__file__), '../../src'))

from src.email_parser import EmailParser

def convert_pdf_to_text(pdf_path):
    """Convert a PDF file to text using pdftotext."""
    result = subprocess.run(['pdftotext', pdf_path, '-'], capture_output=True, text=True)
    return result.stdout

def main():
    """Test the email parser with sample PDFs."""
    attachments_dir = Path.home() / 'attachments'
    pdf_files = []
    
    for subdir in attachments_dir.iterdir():
        if subdir.is_dir():
            for file in subdir.iterdir():
                if file.suffix.lower() == '.pdf':
                    pdf_files.append(file)
    
    if not pdf_files:
        print("No PDF files found in attachments directory")
        return
    
    parser = EmailParser()
    
    for pdf_file in pdf_files[:1]:  # Process just the first PDF for testing
        print(f"\nProcessing {pdf_file.name}")
        
        email_text = convert_pdf_to_text(pdf_file)
        
        regex_data = parser.extract_info_regex(email_text)
        
        print("\nRegex Extraction Results:")
        for key, value in regex_data.items():
            print(f"{key}: {value}")
        
        try:
            ai_data = parser.extract_info_ai(email_text)
            
            print("\nAI Extraction Results:")
            for key, value in ai_data.items():
                print(f"{key}: {value}")
        except Exception as e:
            print(f"\nError in AI extraction: {e}")

if __name__ == "__main__":
    main()
