from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Таблица для хранения местоположений
class Location(models.Model):
    city_name = models.CharField(max_length=100)
    region = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=8, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return f"{self.city_name}, {self.country}"

# Таблица с данными о погоде
class WeatherData(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="weather_data")
    date = models.DateField(default=timezone.now)
    temperature = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    min_temperature = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    max_temperature = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    humidity = models.IntegerField(null=True)
    wind_speed = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    wind_direction = models.CharField(max_length=50, blank=True, null=True)
    precipitation = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    weather_description = models.CharField(max_length=200, blank=True, null=True)
    weather_image = models.CharField(max_length=200, blank=True, null=True)
    def __str__(self):
        return f"Weather on {self.date} in {self.location}"
    
    def get_absolute_url(self):
        return reverse('forecast',  kwargs={'date' : self.date})

# Таблица с прогнозом погоды, включая почасовую информацию
class Forecast(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="forecasts", default=1)
    forecast_date = models.DateField(default=timezone.now)
    forecast_time = models.TimeField(null=True, blank=True)
    max_temperature = models.IntegerField(null=True)
    min_temperature = models.IntegerField(null=True)
    weather = models.CharField(max_length=200, null=True)
    hourly_temperature = models.JSONField(default=dict, null=True)  # Словарь для хранения почасовой температуры
    humidity = models.IntegerField(null=True)
    wind_speed = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    precipitation_chance = models.IntegerField(null=True)
    forecast_description = models.CharField(max_length=200, blank=True, null=True)
    weather_image = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"Forecast for {self.forecast_date} in {self.location}"



class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    
    # Optional fields
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # Timestamps
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'name']

    objects = CustomUserManager()

    def __str__(self):
        return self.username