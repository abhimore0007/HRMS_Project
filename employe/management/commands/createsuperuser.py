from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = "Create a superuser for Employe_User model"

    def handle(self, *args, **kwargs):
        User = get_user_model()

        email = input("Enter email: ")
        first_name = input("Enter first name: ")
        last_name = input("Enter last name: ")
        mobile = input("Enter mobile number: ")
        password = input("Enter password: ")

        if not User.objects.filter(email=email).exists():
            user = User.objects.create_superuser(
                email=email,
                first_name=first_name,
                last_name=last_name,
                mobile=mobile,
                password=password
            )
            self.stdout.write(self.style.SUCCESS(f"Superuser '{email}' created successfully."))
        else:
            self.stdout.write(self.style.WARNING(f"User '{email}' already exists."))
