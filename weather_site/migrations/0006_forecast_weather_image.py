# Generated by Django 5.1.2 on 2024-11-06 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather_site', '0005_location_remove_forecast_date_forecast_forecast_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='forecast',
            name='weather_image',
            field=models.ImageField(blank=True, null=True, upload_to='weather_images/'),
        ),
    ]