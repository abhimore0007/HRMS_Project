# Generated by Django 5.1.5 on 2025-02-14 09:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('department', '0001_initial'),
        ('employe', '0005_alter_user_password'),
        ('roles', '0006_userrole_department'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User',
            new_name='Employe_User',
        ),
    ]
