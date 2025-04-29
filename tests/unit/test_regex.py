"""
Test script to verify the regex extraction functionality with sample PDFs.
This script doesn't require the OpenAI API.
"""
import os
import sys
import subprocess
import re
from pathlib import Path

sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

def convert_pdf_to_text(pdf_path):
    """Convert a PDF file to text using pdftotext."""
    result = subprocess.run(['pdftotext', pdf_path, '-'], capture_output=True, text=True)
    return result.stdout

def extract_info_regex(email_body):
    """Extract information from email body using regex."""
    result = {
        'company_name': '',
        'url': '',
        'industry': '',
        'established_year': '',
        'capital': '',
        'revenue': '',
        'fiscal_year_end': '',
        'employee_count': '',
        'prefecture': '',
        'nearest_station': '',
        'company_overview': ''
    }
    
    company_name_match = re.search(r'【法人名】\s*(.+?)(?=\n|【)', email_body)
    if company_name_match:
        result['company_name'] = company_name_match.group(1).strip()
    
    url_match = re.search(r'【URL】\s*(https?://[^\s]+)', email_body)
    if url_match:
        result['url'] = url_match.group(1).strip()
    
    industry_match = re.search(r'【業界】\s*(.+?)(?=\n|【)', email_body)
    if industry_match:
        result['industry'] = industry_match.group(1).strip()
    
    established_match = re.search(r'【設立】\s*(\d{4}年\d{1,2}月\d{1,2}日)', email_body)
    if established_match:
        result['established_year'] = established_match.group(1).strip()
    
    capital_match = re.search(r'【資本金】\s*([0-9,]+円)', email_body)
    if capital_match:
        result['capital'] = capital_match.group(1).strip()
    
    revenue_match = re.search(r'【売上】\s*(.+?)(?=\n|【)', email_body)
    if revenue_match:
        result['revenue'] = revenue_match.group(1).strip()
    
    fiscal_match = re.search(r'【決算】\s*(\d{1,2}月)', email_body)
    if fiscal_match:
        result['fiscal_year_end'] = fiscal_match.group(1).strip()
    
    employee_match = re.search(r'【社員数】\s*(\d+名)', email_body)
    if employee_match:
        result['employee_count'] = employee_match.group(1).strip()
    
    prefecture_match = re.search(r'【都道府県】\s*(.+?[都道府県])(?=\n|【)', email_body)
    if prefecture_match:
        result['prefecture'] = prefecture_match.group(1).strip()
    
    station_match = re.search(r'【最寄駅】\s*(.+?駅)(?=\n|【)', email_body)
    if station_match:
        result['nearest_station'] = station_match.group(1).strip()
    
    overview_match = re.search(r'【法人概要】\s*([\s\S]+?)(?=\n【|$)', email_body)
    if overview_match:
        result['company_overview'] = overview_match.group(1).strip()
    
    return result

def main():
    """Test the regex extraction with sample PDFs."""
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
    
    for pdf_file in pdf_files[:1]:  # Process just the first PDF for testing
        print(f"\nProcessing {pdf_file.name}")
        
        email_text = convert_pdf_to_text(pdf_file)
        
        regex_data = extract_info_regex(email_text)
        
        print("\nRegex Extraction Results:")
        for key, value in regex_data.items():
            print(f"{key}: {value}")

if __name__ == "__main__":
    main()
