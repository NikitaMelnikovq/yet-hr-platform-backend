# Generated by Django 5.2 on 2025-05-14 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vacancies', '0002_alter_candidateresponse_vacancy'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidateresponse',
            name='archived',
            field=models.BooleanField(default=False),
        ),
    ]
