
sleep 10


echo "Starting Celery beat..."
exec celery -A sqliteapitesting beat --loglevel=info
