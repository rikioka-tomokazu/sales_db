"""
Test script to verify the entire workflow with mock data.
"""
import os
import sys
import json
import logging
from datetime import datetime
from pathlib import Path

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class MockGmailClient:
    """Mock Gmail client for testing."""
    
    def get_emails(self, days=1):
        """Return mock emails."""
        logger.info(f"Getting emails for the last {days} days")
        
        email = {
            'id': 'mock-email-123',
            'subject': 'Ready Crew案件のご紹介',
            'from': 'sender@example.com',
            'to': 'rc_support@frontier-gr.jp',
            'date': datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0900'),
            'body': self._get_mock_email_body()
        }
        
        return [email]
    
    def _get_mock_email_body(self):
        """Return a mock email body."""
        return """
【法人名】株式会社エルハウジング
【URL】https://l-housing.co.jp/
【業界】建設 / 総合建設 / ビル・住宅建築
【設立】2005年4月1日
【資本金】60,000,000円
【売上】13,392,000,000円
【決算】3月
【社員数】122名
【都道府県】京都府
【最寄駅】太秦天神川駅
【法人概要】事業の柱である新築住宅分譲事業において、土地の仕入れから造成・設計・販売・アフターサービスに至るまで社内一貫体制の会社です。
街づくり・リフォーム・賃貸などの「住まい」関連事業に留まらず、現在ではサービス付高齢者住宅（さがの福寿苑にて展開）や、福祉用具の販売・レンタル（ソーケンメディカル社で展開）、工業団地の分譲による雇用創出などの「暮らし」関連へと事業を展開中です。

■案件概要
【案件名】AIを活用した不動産価格予測システムの開発
【契約形態】準委任
【業務内容】
不動産価格予測AIシステムの開発をお願いします。
過去の不動産取引データ、地理情報、周辺施設情報などを活用し、物件の適正価格を予測するAIモデルの構築が主な業務となります。

【必須スキル】
・Python（3年以上）
・機械学習/ディープラーニングの実務経験（2年以上）
・SQLデータベースの知識

【歓迎スキル】
・不動産業界での就業経験
・TensorFlow/PyTorchの使用経験
・GCP/AWSでの開発経験
・Webアプリケーション開発経験

【期間】2023年5月〜長期（6ヶ月〜）
【稼働】週5日（リモート可）
【単価】〜100万円（スキル・経験による）
"""

class MockEmailParser:
    """Mock email parser for testing."""
    
    def extract_info_regex(self, email_body):
        """Extract information using regex."""
        logger.info("Extracting information using regex")
        
        return {
            'company_name': '株式会社エルハウジング',
            'url': 'https://l-housing.co.jp/',
            'industry': '建設 / 総合建設 / ビル・住宅建築',
            'established_year': '2005年4月1日',
            'capital': '60,000,000円',
            'revenue': '13,392,000,000円',
            'fiscal_year_end': '3月',
            'employee_count': '122名',
            'prefecture': '京都府',
            'nearest_station': '太秦天神川駅',
            'company_overview': '事業の柱である新築住宅分譲事業において、土地の仕入れから造成・設計・販売・アフターサービスに至るまで社内一貫体制の会社です。'
        }
    
    def extract_info_ai(self, email_body):
        """Extract information using AI."""
        logger.info("Extracting information using AI")
        
        return {
            'project_type': 'AIを活用した不動産価格予測システムの開発',
            'contract_type': '準委任',
            'industry': '不動産',
            'technologies': 'Python, 機械学習, ディープラーニング, SQL, TensorFlow, PyTorch',
            'data_types': '不動産取引データ, 地理情報, 周辺施設情報',
            'tools_platforms': 'GCP, AWS',
            'project_phases': '開発',
            'roles': 'エンジニア, データサイエンティスト'
        }

class MockBigQueryClient:
    """Mock BigQuery client for testing."""
    
    def create_dataset_if_not_exists(self):
        """Create dataset if it doesn't exist."""
        logger.info("Creating dataset if it doesn't exist")
        return True
    
    def create_table_if_not_exists(self):
        """Create table if it doesn't exist."""
        logger.info("Creating table if it doesn't exist")
        return True
    
    def insert_data(self, email_data, regex_data, ai_data):
        """Insert data into BigQuery."""
        logger.info("Inserting data into BigQuery")
        
        row = {
            "email_id": email_data.get('id', ''),
            "subject": email_data.get('subject', ''),
            "from_email": email_data.get('from', ''),
            "to_email": email_data.get('to', ''),
            "received_date": email_data.get('date', ''),
            "processed_date": datetime.now().isoformat(),
            
            "company_name": regex_data.get('company_name', ''),
            "url": regex_data.get('url', ''),
            "industry": regex_data.get('industry', ''),
            "established_year": regex_data.get('established_year', ''),
            "capital": regex_data.get('capital', ''),
            "revenue": regex_data.get('revenue', ''),
            "fiscal_year_end": regex_data.get('fiscal_year_end', ''),
            "employee_count": regex_data.get('employee_count', ''),
            "prefecture": regex_data.get('prefecture', ''),
            "nearest_station": regex_data.get('nearest_station', ''),
            "company_overview": regex_data.get('company_overview', ''),
            
            "project_type": ai_data.get('project_type', ''),
            "contract_type": ai_data.get('contract_type', ''),
            "ai_industry": ai_data.get('industry', ''),
            "technologies": ai_data.get('technologies', ''),
            "data_types": ai_data.get('data_types', ''),
            "tools_platforms": ai_data.get('tools_platforms', ''),
            "project_phases": ai_data.get('project_phases', ''),
            "roles": ai_data.get('roles', ''),
            
            "email_body": email_data.get('body', '')
        }
        
        logger.info(f"Row data: {json.dumps(row, indent=2, ensure_ascii=False)}")
        
        return True

def test_workflow():
    """Test the entire workflow with mock data."""
    logger.info("Starting workflow test")
    
    gmail_client = MockGmailClient()
    email_parser = MockEmailParser()
    bigquery_client = MockBigQueryClient()
    
    emails = gmail_client.get_emails(days=1)
    logger.info(f"Retrieved {len(emails)} emails")
    
    for email in emails:
        email_id = email.get('id', '')
        logger.info(f"Processing email {email_id}")
        
        regex_data = email_parser.extract_info_regex(email.get('body', ''))
        logger.info(f"Extracted regex data for email {email_id}")
        
        ai_data = email_parser.extract_info_ai(email.get('body', ''))
        logger.info(f"Extracted AI data for email {email_id}")
        
        success = bigquery_client.insert_data(email, regex_data, ai_data)
        if success:
            logger.info(f"Successfully inserted data for email {email_id}")
        else:
            logger.error(f"Failed to insert data for email {email_id}")
    
    logger.info("Workflow test completed successfully")

if __name__ == "__main__":
    test_workflow()
