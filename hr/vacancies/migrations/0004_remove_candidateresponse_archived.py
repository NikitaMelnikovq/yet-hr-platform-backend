# Generated by Django 5.2 on 2025-05-14 12:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vacancies', '0003_candidateresponse_archived'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='candidateresponse',
            name='archived',
        ),
    ]
