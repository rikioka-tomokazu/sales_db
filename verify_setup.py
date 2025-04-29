"""
Verification script to test the Gmail to BigQuery setup.
"""
import os
import sys
from pathlib import Path
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def check_file_exists(file_path, required=True):
    """Check if a file exists and log the result."""
    path = Path(file_path)
    if path.exists():
        logger.info(f"✓ {file_path} exists")
        return True
    else:
        if required:
            logger.error(f"✗ {file_path} does not exist")
        else:
            logger.warning(f"! {file_path} does not exist (optional)")
        return False

def check_env_variables():
    """Check if environment variables are set."""
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = [
        'GMAIL_CREDENTIALS_FILE',
        'GMAIL_TOKEN_FILE',
        'GMAIL_TARGET_EMAIL',
        'GOOGLE_APPLICATION_CREDENTIALS',
        'BIGQUERY_PROJECT_ID',
        'BIGQUERY_DATASET_ID',
        'BIGQUERY_TABLE_ID'
    ]
    
    optional_vars = [
        'OPENAI_API_KEY'
    ]
    
    all_required_set = True
    for var in required_vars:
        if os.getenv(var):
            logger.info(f"✓ Environment variable {var} is set")
        else:
            logger.error(f"✗ Environment variable {var} is not set")
            all_required_set = False
    
    for var in optional_vars:
        if os.getenv(var):
            logger.info(f"✓ Optional environment variable {var} is set")
        else:
            logger.warning(f"! Optional environment variable {var} is not set")
    
    return all_required_set

def check_credentials():
    """Check if credential files exist."""
    from dotenv import load_dotenv
    load_dotenv()
    
    gmail_creds = os.getenv('GMAIL_CREDENTIALS_FILE', 'credentials.json')
    gmail_token = os.getenv('GMAIL_TOKEN_FILE', 'token.json')
    bq_creds = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', 'bigquery-credentials.json')
    
    gmail_creds_exist = check_file_exists(gmail_creds)
    gmail_token_exist = check_file_exists(gmail_token, required=False)
    bq_creds_exist = check_file_exists(bq_creds)
    
    return gmail_creds_exist and bq_creds_exist

def check_imports():
    """Check if required packages are installed."""
    required_packages = [
        'google.auth',
        'googleapiclient',
        'google.cloud.bigquery',
        'dotenv',
        'schedule'
    ]
    
    optional_packages = [
        'openai'
    ]
    
    all_required_installed = True
    for package in required_packages:
        try:
            __import__(package.split('.')[0])
            logger.info(f"✓ Package {package} is installed")
        except ImportError:
            logger.error(f"✗ Package {package} is not installed")
            all_required_installed = False
    
    for package in optional_packages:
        try:
            __import__(package)
            logger.info(f"✓ Optional package {package} is installed")
        except ImportError:
            logger.warning(f"! Optional package {package} is not installed")
    
    return all_required_installed

def main():
    """Run verification checks."""
    logger.info("Starting verification of Gmail to BigQuery setup")
    
    src_dir = Path('src')
    if not src_dir.exists():
        logger.error("✗ src directory does not exist")
        return False
    
    files_to_check = [
        'src/gmail_client.py',
        'src/email_parser.py',
        'src/bigquery_client.py',
        'src/main.py',
        'requirements.txt',
        '.env.example'
    ]
    
    all_files_exist = True
    for file in files_to_check:
        if not check_file_exists(file):
            all_files_exist = False
    
    if not all_files_exist:
        logger.error("✗ Some required files are missing")
        return False
    
    env_file_exists = check_file_exists('.env', required=False)
    if not env_file_exists:
        logger.warning("! .env file does not exist. Creating from example...")
        try:
            with open('.env.example', 'r') as example_file:
                with open('.env', 'w') as env_file:
                    env_file.write(example_file.read())
            logger.info("✓ Created .env file from example")
        except Exception as e:
            logger.error(f"✗ Failed to create .env file: {e}")
            return False
    
    env_vars_set = check_env_variables()
    if not env_vars_set:
        logger.error("✗ Some required environment variables are not set")
        logger.info("! Please edit the .env file to set all required variables")
    
    creds_exist = check_credentials()
    if not creds_exist:
        logger.error("✗ Some required credential files are missing")
        logger.info("! Please place the credential files in the project directory")
    
    imports_ok = check_imports()
    if not imports_ok:
        logger.error("✗ Some required packages are not installed")
        logger.info("! Please run 'pip install -r requirements.txt' to install all required packages")
    
    if all_files_exist and env_vars_set and creds_exist and imports_ok:
        logger.info("✓ All checks passed! The setup is complete.")
        logger.info("✓ You can now run the script with 'python src/main.py --run-now'")
        return True
    else:
        logger.warning("! Some checks failed. Please fix the issues before running the script.")
        return False

if __name__ == "__main__":
    main()
