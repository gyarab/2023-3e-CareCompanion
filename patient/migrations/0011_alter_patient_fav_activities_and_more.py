# Generated by Django 4.2.8 on 2024-03-16 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0010_alter_patient_date_of_admission'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='fav_activities',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='patient',
            name='health_info',
            field=models.TextField(),
        ),
    ]
