# Generated by Django 4.2.8 on 2024-02-16 11:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0008_alter_patient_date_of_admission'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='date_of_admission',
            field=models.DateField(default=datetime.datetime(2024, 2, 16, 12, 48, 26, 804877)),
        ),
    ]
