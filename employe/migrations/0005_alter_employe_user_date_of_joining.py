# Generated by Django 5.1.5 on 2025-02-18 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employe', '0004_alter_employe_user_date_of_joining'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employe_user',
            name='date_of_joining',
            field=models.DateField(blank=True, default='2025-01-01', null=True),
        ),
    ]
