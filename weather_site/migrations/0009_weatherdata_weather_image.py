# Generated by Django 5.1.2 on 2024-11-06 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather_site', '0008_alter_forecast_weather_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='weatherdata',
            name='weather_image',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
