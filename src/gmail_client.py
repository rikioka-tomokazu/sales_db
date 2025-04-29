"""
Gmail API client for fetching emails from a specific email address.
"""
import os
import base64
import re
from typing import List, Dict, Any, Optional
from email.message import EmailMessage
import pickle
from pathlib import Path
from datetime import datetime, timedelta

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

class GmailClient:
    """Client for interacting with Gmail API."""

    def __init__(self):
        """Initialize the Gmail API client."""
        self.credentials_file = os.getenv('GMAIL_CREDENTIALS_FILE', 'credentials.json')
        self.token_file = os.getenv('GMAIL_TOKEN_FILE', 'token.json')
        self.target_email = os.getenv('GMAIL_TARGET_EMAIL', 'rc_support@frontier-gr.jp')
        self.service = self._get_gmail_service()

    def _get_gmail_service(self):
        """Authenticate and build the Gmail service."""
        creds = None

        if os.path.exists(self.token_file):
            with open(self.token_file, 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, SCOPES)
                creds = flow.run_local_server(port=0)

            with open(self.token_file, 'wb') as token:
                pickle.dump(creds, token)

        return build('gmail', 'v1', credentials=creds)

    def get_emails(self, days: int = 1) -> List[Dict[str, Any]]:
        """
        Get emails from the target email address within the specified time period.

        Args:
            days: Number of days to look back for emails

        Returns:
            List of email data dictionaries
        """
        after_date = (datetime.now() - timedelta(days=days)).strftime('%Y/%m/%d')

        query = f"to:{self.target_email} after:{after_date}"

        results = self.service.users().messages().list(userId='me', q=query).execute()
        messages = results.get('messages', [])

        emails = []
        for message in messages:
            msg = self.service.users().messages().get(userId='me', id=message['id']).execute()

            headers = {header['name']: header['value'] for header in msg['payload']['headers']}

            body = self._get_email_body(msg)

            email_data = {
                'id': message['id'],
                'subject': headers.get('Subject', ''),
                'from': headers.get('From', ''),
                'to': headers.get('To', ''),
                'date': headers.get('Date', ''),
                'body': body
            }

            emails.append(email_data)

        return emails

    def _get_email_body(self, message: Dict[str, Any]) -> str:
        """
        Extract the email body from the message.

        Args:
            message: The Gmail API message object

        Returns:
            The email body as text
        """
        if 'parts' in message['payload']:
            for part in message['payload']['parts']:
                if part['mimeType'] == 'text/plain':
                    if 'data' in part['body']:
                        return base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')

        if 'body' in message['payload'] and 'data' in message['payload']['body']:
            return base64.urlsafe_b64decode(message['payload']['body']['data']).decode('utf-8')

        return ""
