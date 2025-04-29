"""
Email parser module for extracting information from email content using regex.
"""
import re
from typing import Dict, Any, Optional, List
import openai
import os
from dotenv import load_dotenv

load_dotenv()

class EmailParser:
    """Parser for extracting information from email content."""
    
    def __init__(self):
        """Initialize the email parser."""
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        if self.openai_api_key:
            openai.api_key = self.openai_api_key
    
    def extract_info_regex(self, email_body: str) -> Dict[str, Any]:
        """
        Extract information from email body using regex.
        
        Args:
            email_body: The email body text
            
        Returns:
            Dictionary with extracted information
        """
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
    
    def extract_info_ai(self, email_body: str) -> Dict[str, Any]:
        """
        Extract information from email body using AI.
        
        Args:
            email_body: The email body text
            
        Returns:
            Dictionary with extracted information
        """
        if not self.openai_api_key:
            return {
                'project_type': '',
                'contract_type': '',
                'industry': '',
                'technologies': '',
                'data_types': '',
                'tools_platforms': '',
                'project_phases': '',
                'roles': ''
            }
        
        prompt = f"""
        以下のメール本文から、案件に関する情報を抽出してください。
        
        抽出項目:
        1. 案件種別 (例: 新規開発、保守運用、コンサルティングなど)
        2. 契約形態 (例: 準委任、請負など)
        3. 業界 (例: 金融、医療、小売など)
        4. 使用技術 (例: Python、Java、TensorFlow、PyTorchなど)
        5. 使用データ (例: 顧客データ、センサーデータ、画像データなど)
        6. 使用ツール・基盤 (例: AWS、GCP、Azure、Kubernetesなど)
        7. 担当フェーズ (例: 要件定義、設計、開発、テスト、運用など)
        8. 担当役割 (例: PM、エンジニア、データサイエンティストなど)
        
        メール本文:
        {email_body}
        
        JSON形式で回答してください。情報が見つからない場合はnullとしてください。
        """
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "あなたはメール本文から情報を抽出するAIアシスタントです。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            ai_response = response.choices[0].message.content
            
            import json
            try:
                extracted_info = json.loads(ai_response)
            except json.JSONDecodeError:
                json_match = re.search(r'```json\n([\s\S]+?)\n```', ai_response)
                if json_match:
                    extracted_info = json.loads(json_match.group(1))
                else:
                    extracted_info = {
                        'project_type': '',
                        'contract_type': '',
                        'industry': '',
                        'technologies': '',
                        'data_types': '',
                        'tools_platforms': '',
                        'project_phases': '',
                        'roles': ''
                    }
            
            return {
                'project_type': extracted_info.get('案件種別'),
                'contract_type': extracted_info.get('契約形態'),
                'industry': extracted_info.get('業界'),
                'technologies': extracted_info.get('使用技術'),
                'data_types': extracted_info.get('使用データ'),
                'tools_platforms': extracted_info.get('使用ツール・基盤'),
                'project_phases': extracted_info.get('担当フェーズ'),
                'roles': extracted_info.get('担当役割')
            }
            
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            return {
                'project_type': '',
                'contract_type': '',
                'industry': '',
                'technologies': '',
                'data_types': '',
                'tools_platforms': '',
                'project_phases': '',
                'roles': ''
            }
