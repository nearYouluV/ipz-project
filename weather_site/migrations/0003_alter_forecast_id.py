# Generated by Django 5.1.2 on 2024-10-30 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather_site', '0002_alter_forecast_date_alter_forecast_max_temperature_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forecast',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
