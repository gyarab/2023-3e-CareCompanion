# Generated by Django 5.0.1 on 2024-01-30 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caregiver', '0006_alter_caregiver_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='caregiver',
            name='first_name',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='caregiver',
            name='surname',
            field=models.CharField(max_length=150),
        ),
    ]
