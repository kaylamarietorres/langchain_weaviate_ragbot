#!/bin/bash
set -e

# Create migrations if there are changes
python manage.py makemigrations

# Apply database migrations
python manage.py migrate

# Check if superuser exists, create if not
echo "Checking for superuser..."
python manage.py shell <<EOF
from django.contrib.auth.models import User
from django.core.management import call_command

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    print('Superuser created.')
else:
    print('Superuser already exists.')
EOF

# Start the server
exec "$@"
