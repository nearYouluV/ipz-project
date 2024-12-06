import requests
from .models import *
from datetime import datetime
import random
def get_location_key(location_name):
    params = {
        'apikey': 'qMjRLR8urIVDihYY5ksZhzfa5Xqx5Wnu',
        'q': f'{location_name}',
        # 'offset' : 1
    }
    response = requests.get('http://dataservice.accuweather.com/locations/v1/cities/search', params=params)
    print(response)
    if response.status_code == 200:
        item = response.json()[0]
        obj, created = Location.objects.update_or_create(
            # id = item['location_']
            city_name=f"{location_name}",
            region=f"{item['AdministrativeArea']['EnglishName']}, {item['Country']['EnglishName']}",
            country=f"{item['Country']['EnglishName']}",
            latitude=item['GeoPosition']['Latitude'],
            longitude=item['GeoPosition']['Longitude']
        )

        return {
                'location_key' : response.json()[0]['Key'],
                'location_name' : location_name,
                'location_obj' : obj
            }

# get_location_key('London')


def get_location_5day_forecast(location_info:dict):
    location_key = location_info['location_key']
    
    # location_id = location_info['location_id']
    location = location_info['location_obj']
    
    params = {
        'apikey': 'qMjRLR8urIVDihYY5ksZhzfa5Xqx5Wnu',
        'metric': 'true',
        'details' : 'true'
    }
    response = requests.get(f'http://dataservice.accuweather.com/forecasts/v1/daily/5day/{location_key}', params=params)
    for item in response.json()["DailyForecasts"]:
        print(item["Date"])
        # WeatherData.objects.filter(location=location, date=datetime.fromisoformat(item["Date"])).exists()
        WeatherData.objects.update_or_create(
                location=location,
                date=datetime.fromisoformat(item["Date"]),
                temperature=0,
                min_temperature=item["Temperature"]["Minimum"]["Value"],
                max_temperature=item["Temperature"]["Maximum"]["Value"],
                humidity=item["Day"]["RelativeHumidity"].get("Average", 0),
                wind_speed=item["Day"]["Wind"]["Speed"]["Value"],
                wind_direction=item["Day"]["Wind"]["Direction"]["English"],
                precipitation=item["Day"]["PrecipitationProbability"],
                weather_description= item["Day"]["IconPhrase"],
                weather_image = f"https://www.accuweather.com/images/weathericons/{item['Day']['Icon']}.svg"
            )
        max_temp = 15.0
        min_temp = 8.0
        hourly_temp = {
                "00:00": random.randint(min_temp, max_temp),
                "06:00": random.randint(min_temp, max_temp),
                "12:00": max_temp,
                "15:00": random.randint(min_temp, max_temp),
                "18:00": random.randint(min_temp, max_temp),
                "21:00": min_temp,
            }
        Forecast.objects.update_or_create(
                location=location,
                forecast_date=datetime.fromisoformat(item["Date"]),
                min_temperature=item["Temperature"]["Minimum"]["Value"],
                max_temperature=item["Temperature"]["Maximum"]["Value"],
                weather= item["Day"]["ShortPhrase"],
                hourly_temperature=hourly_temp,
                humidity=item["Day"]["RelativeHumidity"].get("Average", 0),
                wind_speed=item["Day"]["Wind"]["Speed"]["Value"],
                precipitation_chance= item["Day"]["PrecipitationProbability"],
                forecast_description="Partly cloudy with a chance of light rain in the evening."
            )
            
def get_weather_by_location(city):
    get_location_5day_forecast(get_location_key(city))

if __name__ == '__main__':
    get_weather_by_location('London')
