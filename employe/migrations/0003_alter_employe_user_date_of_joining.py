# Generated by Django 5.1.5 on 2025-02-18 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employe', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employe_user',
            name='date_of_joining',
            field=models.DateField(default='2025-01-01'),
        ),
    ]
