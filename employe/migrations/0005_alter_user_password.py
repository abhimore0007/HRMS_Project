# Generated by Django 5.1.5 on 2025-02-14 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employe', '0004_delete_employee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=128),
        ),
    ]
