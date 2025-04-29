"""
BigQuery client for storing extracted email information.
"""
import os
from typing import Dict, Any, List
from google.cloud import bigquery
from dotenv import load_dotenv

load_dotenv()

class BigQueryClient:
    """Client for interacting with BigQuery."""
    
    def __init__(self):
        """Initialize the BigQuery client."""
        self.project_id = os.getenv('BIGQUERY_PROJECT_ID', '')
        self.dataset_id = os.getenv('BIGQUERY_DATASET_ID', 'email_data')
        self.table_id = os.getenv('BIGQUERY_TABLE_ID', 'extracted_info')
        self.client = bigquery.Client(project=self.project_id)
        
    def create_dataset_if_not_exists(self):
        """Create the dataset if it doesn't exist."""
        dataset_ref = self.client.dataset(self.dataset_id)
        
        try:
            self.client.get_dataset(dataset_ref)
            print(f"Dataset {self.dataset_id} already exists")
        except Exception:
            dataset = bigquery.Dataset(dataset_ref)
            dataset.location = "asia-northeast1"  # Tokyo region
            dataset = self.client.create_dataset(dataset)
            print(f"Dataset {self.dataset_id} created")
    
    def create_table_if_not_exists(self):
        """Create the table if it doesn't exist."""
        dataset_ref = self.client.dataset(self.dataset_id)
        table_ref = dataset_ref.table(self.table_id)
        
        try:
            self.client.get_table(table_ref)
            print(f"Table {self.table_id} already exists")
        except Exception:
            schema = [
                bigquery.SchemaField("email_id", "STRING", mode="REQUIRED", description="Email ID"),
                bigquery.SchemaField("subject", "STRING", description="Email subject"),
                bigquery.SchemaField("from_email", "STRING", description="Sender email"),
                bigquery.SchemaField("to_email", "STRING", description="Recipient email"),
                bigquery.SchemaField("received_date", "TIMESTAMP", description="Date email was received"),
                bigquery.SchemaField("processed_date", "TIMESTAMP", description="Date email was processed"),
                
                bigquery.SchemaField("company_name", "STRING", description="法人名"),
                bigquery.SchemaField("url", "STRING", description="URL"),
                bigquery.SchemaField("industry", "STRING", description="業界"),
                bigquery.SchemaField("established_year", "STRING", description="設立年"),
                bigquery.SchemaField("capital", "STRING", description="資本金"),
                bigquery.SchemaField("revenue", "STRING", description="売上"),
                bigquery.SchemaField("fiscal_year_end", "STRING", description="決算月"),
                bigquery.SchemaField("employee_count", "STRING", description="社員数"),
                bigquery.SchemaField("prefecture", "STRING", description="所在地（都道府県）"),
                bigquery.SchemaField("nearest_station", "STRING", description="最寄り駅"),
                bigquery.SchemaField("company_overview", "STRING", description="法人概要"),
                
                bigquery.SchemaField("project_type", "STRING", description="案件種別"),
                bigquery.SchemaField("contract_type", "STRING", description="契約形態"),
                bigquery.SchemaField("ai_industry", "STRING", description="業界 (AI抽出)"),
                bigquery.SchemaField("technologies", "STRING", description="使用技術"),
                bigquery.SchemaField("data_types", "STRING", description="使用データ"),
                bigquery.SchemaField("tools_platforms", "STRING", description="使用ツール・基盤"),
                bigquery.SchemaField("project_phases", "STRING", description="担当フェーズ"),
                bigquery.SchemaField("roles", "STRING", description="担当役割"),
                
                bigquery.SchemaField("email_body", "STRING", description="Raw email body")
            ]
            
            table = bigquery.Table(table_ref, schema=schema)
            table = self.client.create_table(table)
            print(f"Table {self.table_id} created")
    
    def insert_data(self, email_data: Dict[str, Any], regex_data: Dict[str, Any], ai_data: Dict[str, Any]) -> bool:
        """
        Insert extracted data into BigQuery.
        
        Args:
            email_data: Email metadata
            regex_data: Data extracted using regex
            ai_data: Data extracted using AI
            
        Returns:
            True if successful, False otherwise
        """
        from datetime import datetime
        
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
        
        table_ref = self.client.dataset(self.dataset_id).table(self.table_id)
        errors = self.client.insert_rows_json(table_ref, [row])
        
        if errors:
            print(f"Errors inserting row: {errors}")
            return False
        
        return True
    
    def insert_batch_data(self, rows: List[Dict[str, Any]]) -> bool:
        """
        Insert multiple rows of data into BigQuery.
        
        Args:
            rows: List of row dictionaries to insert
            
        Returns:
            True if successful, False otherwise
        """
        table_ref = self.client.dataset(self.dataset_id).table(self.table_id)
        errors = self.client.insert_rows_json(table_ref, rows)
        
        if errors:
            print(f"Errors inserting rows: {errors}")
            return False
        
        return True
