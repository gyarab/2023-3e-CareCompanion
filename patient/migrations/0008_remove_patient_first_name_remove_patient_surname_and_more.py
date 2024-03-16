# Generated by Django 5.0.2 on 2024-03-15 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0007_patient_date_of_admission'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='surname',
        ),
        migrations.AlterField(
            model_name='patient',
            name='date_of_admission',
            field=models.DateField(default='2024-01-01'),
        ),
    ]