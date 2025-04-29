"""
Main script for fetching emails, extracting information, and storing in BigQuery.
"""
import os
import sys
import time
import logging
from datetime import datetime
from typing import List, Dict, Any
import schedule

from gmail_client import GmailClient
from email_parser import EmailParser
from bigquery_client import BigQueryClient

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("email_processor.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def process_emails(days: int = 1) -> None:
    """
    Process emails from the last specified number of days.
    
    Args:
        days: Number of days to look back for emails
    """
    logger.info(f"Starting email processing for the last {days} days")
    
    try:
        gmail_client = GmailClient()
        email_parser = EmailParser()
        bigquery_client = BigQueryClient()
        
        bigquery_client.create_dataset_if_not_exists()
        bigquery_client.create_table_if_not_exists()
        
        emails = gmail_client.get_emails(days=days)
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
        
        logger.info("Email processing completed successfully")
    
    except Exception as e:
        logger.error(f"Error processing emails: {e}")

def run_daily_job() -> None:
    """Run the daily job to process emails."""
    logger.info("Running daily job")
    process_emails(days=1)
    logger.info("Daily job completed")

def schedule_daily_job(hour: int = 1, minute: int = 0) -> None:
    """
    Schedule the daily job to run at the specified time.
    
    Args:
        hour: Hour to run the job (24-hour format)
        minute: Minute to run the job
    """
    schedule.every().day.at(f"{hour:02d}:{minute:02d}").do(run_daily_job)
    logger.info(f"Scheduled daily job to run at {hour:02d}:{minute:02d}")
    
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Process emails and store in BigQuery")
    parser.add_argument("--days", type=int, default=1, help="Number of days to look back for emails")
    parser.add_argument("--schedule", action="store_true", help="Schedule daily job")
    parser.add_argument("--hour", type=int, default=1, help="Hour to run the daily job (24-hour format)")
    parser.add_argument("--minute", type=int, default=0, help="Minute to run the daily job")
    parser.add_argument("--run-now", action="store_true", help="Run the job immediately")
    
    args = parser.parse_args()
    
    if args.run_now:
        process_emails(days=args.days)
    
    if args.schedule:
        schedule_daily_job(hour=args.hour, minute=args.minute)
