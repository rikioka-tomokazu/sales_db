

cd "$(dirname "$0")"


python src/main.py --days 1 --run-now

echo "$(date): Daily job completed" >> email_processor.log
