import os
import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "company.settings")  # Replace with your actual project name
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Fetch superuser credentials from environment variables
username = os.getenv("DJANGO_SUPERUSER_USERNAME", "admin")
email = os.getenv("DJANGO_SUPERUSER_EMAIL", "admin@gmail.com")
password = os.getenv("DJANGO_SUPERUSER_PASSWORD", "Admin@123")

# Create superuser if it doesn't already exist
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print("✅ Superuser created successfully!")
else:
    print("⚠️ Superuser already exists!")
