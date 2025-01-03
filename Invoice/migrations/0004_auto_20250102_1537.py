# Generated by Django 5.1.4 on 2025-01-02 05:37

import uuid
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('Invoice', '0003_unique_id_generator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='letter_information',
            name='letter_id',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
    ]