# Generated by Django 5.0.2 on 2024-02-11 12:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caregiver', '0010_caregiver_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='caregiver',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2024, 2, 11, 13, 53, 21, 295521)),
        ),
    ]
