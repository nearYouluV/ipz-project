# from django.utils import timezone
# from datetime import timedelta
# import random
# from django.utils import timezone
# from .models import Location, Forecast, WeatherData
# from datetime import timedelta
# import random

# import random
# from datetime import timedelta
# from django.utils import timezone
# from .models import Location, WeatherData, Forecast

# def populate_lviv_weather_and_forecast():
#     # Check if Lviv already exists, or create it
#     lviv, created = Location.objects.get_or_create(
#         city_name="Lviv",
#         region="Lviv Oblast",
#         country="Ukraine",
#         latitude=49.8397,
#         longitude=24.0297
#     )

#     # Populate weather and forecast data for the next 10 days
#     for i in range(10):
#         date = timezone.now().date() + timedelta(days=i)
        
#         # Check if WeatherData entry exists for this date
#         if not WeatherData.objects.filter(location=lviv, date=date).exists():
#             # Randomized current weather data
#             current_temp = random.randint(5, 15)
#             WeatherData.objects.create(
#                 location=lviv,
#                 date=date,
#                 temperature=current_temp,
#                 min_temperature=current_temp - random.randint(0, 5),
#                 max_temperature=current_temp + random.randint(0, 5),
#                 humidity=random.randint(50, 90),
#                 wind_speed=random.uniform(1.0, 5.0),
#                 wind_direction=random.choice(["N", "NE", "E", "SE", "S", "SW", "W", "NW"]),
#                 precipitation=random.uniform(0.0, 5.0),
#                 weather_description="Clear skies with occasional clouds."
#             )

#         # Check if Forecast entry exists for this date
#         if not Forecast.objects.filter(location=lviv, forecast_date=date).exists():
#             # Randomized forecast data for demonstration purposes
#             max_temp = random.randint(10, 20)
#             min_temp = random.randint(0, 10)
#             hourly_temp = {
#                 "00:00": random.randint(min_temp, max_temp),
#                 "06:00": random.randint(min_temp, max_temp),
#                 "12:00": max_temp,
#                 "15:00": random.randint(min_temp, max_temp),
#                 "18:00": random.randint(min_temp, max_temp),
#                 "21:00": min_temp,
#             }

#             # Create forecast
#             Forecast.objects.create(
#                 location=lviv,
#                 forecast_date=date,
#                 max_temperature=max_temp,
#                 min_temperature=min_temp,
#                 weather="Partly Cloudy",
#                 hourly_temperature=hourly_temp,
#                 humidity=random.randint(60, 90),
#                 wind_speed=random.uniform(1.0, 5.0),
#                 precipitation_chance=random.randint(0, 50),
#                 forecast_description="Partly cloudy with a chance of light rain in the evening."
#             )

#     print("Weather and forecast data for the next 10 days in Lviv has been populated.")

# # Call the function to populate data
# populate_lviv_weather_and_forecast()
