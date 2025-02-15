# Generated by Django 5.1.5 on 2025-02-15 09:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('employe', '0006_rename_user_employe_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_title', models.CharField(max_length=100)),
                ('task_description', models.TextField(blank=True, max_length=300, null=True)),
                ('task_priority', models.CharField(choices=[('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')], default='Medium', max_length=10)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('task_type', models.CharField(choices=[('Individual', 'Individual'), ('Team', 'Team')], default='Individual', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='TaskAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assigned_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('In Progress', 'In Progress'), ('Completed', 'Completed')], default='Pending', max_length=15)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('assigned_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tasks_assigned', to='employe.employe_user')),
                ('assigned_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assigned_tasks', to='employe.employe_user')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignments', to='task.task')),
            ],
        ),
    ]
