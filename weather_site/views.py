from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseNotFound, Http404
from datetime import datetime
from urllib.parse import urlencode
from django.urls import reverse, reverse_lazy
from .models import Forecast, Location, WeatherData
from .get_weather_data import get_weather_by_location
from django.views.generic import ListView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.utils import timezone
from datetime import timedelta
from .models import WeatherData
from .forms import SignUpForm, LoginForm
from django.views.generic import CreateView
from django.contrib.auth import login
from django.db.models import F, ExpressionWrapper, IntegerField



class MainPage(ListView):
    model = WeatherData
    template_name = 'weather/index.html'
    context_object_name = 'weather_data'

    def get(self, request, *args, **kwargs):
        # Redirect to the current date URL if no specific date is provided in the URL
        if 'date' not in kwargs:
            current_date = timezone.now().date()
            formatted_date = current_date.strftime('%Y-%m-%d')
            city = request.GET.get('city', 'Lviv')  # Default city is Lviv
            return redirect(f'/{formatted_date}/?city={city}')
        return super().get(request, *args, **kwargs)

    def get_location(self, city_name):
        """Helper method to retrieve or create a Location instance for the specified city."""
        location = Location.objects.filter(city_name__iexact=city_name).first()
        
        # If location is not found, try to fetch it using external API
        if not location:
            get_weather_by_location(city_name)  # Assume this fetches and creates location data
            location = Location.objects.filter(city_name__iexact=city_name).first()
            if not location:
                raise Http404('Location data not found')
        
        return location

    def get_queryset(self):
        # Get the requested city name or default to 'Lviv'
        city_name = self.request.GET.get('city', 'Lviv')
        location = self.get_location(city_name)
        
        # Fetch weather data for the specified location within a 4-day range
        today = timezone.now().date()
        five_day_forecast = WeatherData.objects.annotate(day=ExpressionWrapper(F('date__day') % 2, output_field=IntegerField())).filter(
            location=location,
            date__range=[today, today + timedelta(days=4)],
            day=1
        ).order_by('-date')

        if len(five_day_forecast) == 5:
            return five_day_forecast
        else:
            get_weather_by_location(location)

            five_day_forecast = WeatherData.objects.annotate(day=ExpressionWrapper(F('date__day') % 2, output_field=IntegerField())).filter(
                location=location,
                date__range=[today, today + timedelta(days=4)],
                day=1
            ).order_by('-date')
            return five_day_forecast
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Retrieve city name and selected date from the request
        city_name = self.request.GET.get('city', 'Lviv')
        location = self.get_location(city_name)
        selected_date = self.kwargs['date']

        # Get the current weather for the selected date
        context['current_weather'] = WeatherData.objects.filter(
            location=location,
            date=selected_date,
            
        ).first()
        
        # Include current time, city name, and other required context variables
        context['current_time'] = timezone.now().strftime("%H:%M")
        context['city_name'] = city_name
        
        return context

class ArchivePage(ListView):
    model = WeatherData
    template_name = 'weather/archive.html'
    context_object_name = 'archive_data'
    paginate_by = 9  # Optional: Add pagination if there’s a lot of data

    def get_queryset(self):
        # Get city name and date range from GET parameters
        city_name = self.request.GET.get('city')  # No default city; show all if not specified
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        
        # Retrieve location, but allow results for all cities if no city specified
        if city_name:
            location = Location.objects.filter(city_name__iexact=city_name).first()
            if not location:
                raise Http404('Location not found')
            location_filter = {'location': location}
        else:
            location_filter = {}  # No filtering on location if no city specified

        # Start and end dates fallback to a default range if not provided
        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        else:
            start_date = timezone.now().date() - timedelta(days=30)  # Default to last 30 days

        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        else:
            end_date = timezone.now().date()

        # Filter weather data by location and date range
        return WeatherData.objects.filter(
            **location_filter,
            date__range=(start_date, end_date),
        ).order_by('-date')  # Order by date, descending for archive view

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['city_name'] = self.request.GET.get('city')
        context['start_date'] = self.request.GET.get('start_date')
        context['end_date'] = self.request.GET.get('end_date')
        return context

class SignupPage(CreateView):
    form_class = SignUpForm
    template_name = 'weather/signup.html'

    def form_valid(self, form):
        self.object = form.save()
        login(self.request, self.object)
        print(f"User logged in: {self.request.user}")
        return redirect(reverse_lazy('forecast'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for field in ('first_name','username', 'email', 'password1', 'password2'):
            context['form'].fields[field].widget.attrs.update({
                'class': 'form-control',
                'placeholder': f'Enter {field.capitalize().replace("_", " ")}'
            })
        return context


class LoginPage(LoginView):
    template_name = 'weather/login.html'  # Specify the template to render
    redirect_authenticated_user = True  # Redirect authenticated users to a specific page
    authentication_form = LoginForm  # Use your custom LoginForm (optional)

    def dispatch(self, request, *args, **kwargs):
        # If user is authenticated, redirect to forecast page
        if request.user.is_authenticated:
            return redirect('forecast')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('forecast')  # Redirect to the home page after successful login

class LogoutPage(LogoutView):
    template_name = 'weather/logout.html'  # Custom logout page template

    def dispatch(self, request, *args, **kwargs):
        # Optionally, add any custom actions before logging out, such as a message
        # For example, you can add a message to be displayed on the template
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        # Redirect to login page or any other page after logout
        return reverse_lazy('login')

class AccountPage(TemplateView):
    template_name = 'weather/account.html'  # Specify the template for the account page
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user  # Add user information to the context
        return context
    
    
def page_not_found(request, exception):
    return render(request, 'weather/404.html', status=404)


def server_error(request):
    """
    Custom view to handle 500 errors.
    """
    return render(request, 'weather/500.html', status=500)
    