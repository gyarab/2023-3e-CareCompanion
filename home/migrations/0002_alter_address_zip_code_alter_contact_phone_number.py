# Generated by Django 5.0.2 on 2024-04-13 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='zip_code',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='contact',
            name='phone_number',
            field=models.CharField(max_length=50),
        ),
    ]
