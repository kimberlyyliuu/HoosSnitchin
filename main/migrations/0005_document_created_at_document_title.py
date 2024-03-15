# Generated by Django 5.0.2 on 2024-03-15 18:07

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_remove_report_document_report_document'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='document',
            name='title',
            field=models.CharField(default='No title', max_length=100),
        ),
    ]
