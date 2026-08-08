from typing import Any, Optional
from ast import parse
from celery import shared_task
from .models import Weather
import requests
from .utils import get_weather_category
from django.utils.dateparse import parse_datetime

@shared_task
def fetch_weather_and_cleanup() -> None:
    url: str = "https://api.open-meteo.com/v1/forecast?latitude=30.0626&longitude=31.2497&current=temperature_2m,weather_code&timezone=Africa%2FCairo"
    response: dict[str, Any] = requests.get(url).json()
    
    current_weather: dict[str, Any] = response.get('current', {})
    current_temp: Optional[float] = current_weather.get('temperature_2m')
    weathercode: Optional[int] = current_weather.get('weather_code')
    current_time: Optional[str] = current_weather.get('time')
    
    
    weather_desc: str = get_weather_category(weathercode)
    
   
    if current_temp is not None:
        Weather.objects.create(
            temp=current_temp,
            weather=weather_desc,
            time=parse_datetime(current_time),
            weather_code = weathercode
        )
        print(f"Weather Created: {current_temp} {weather_desc} {parse_datetime(current_time)}")
    
    
    MAX_RECORDS: int = 1000
    

    old_records = Weather.objects.all()[MAX_RECORDS:].values_list('id', flat=True)
    
    if old_records:
        Weather.objects.filter(id__in=old_records).delete()
