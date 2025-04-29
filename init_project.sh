

echo "Creating virtual environment..."
python -m venv venv
source venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

if [ ! -f .env ]; then
    echo "Creating .env file from example..."
    cp .env.example .env
    echo "Please edit .env file with your credentials"
fi

mkdir -p credentials

echo "Project initialized successfully!"
echo "Next steps:"
echo "1. Edit .env file with your credentials"
echo "2. Place Gmail API credentials in credentials.json"
echo "3. Place BigQuery credentials in bigquery-credentials.json"
echo "4. Run 'python src/main.py --run-now' to test the setup"
