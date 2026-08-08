# pyrefly: ignore [missing-import]
from typing import Optional, Any
from django.http import HttpRequest, HttpResponse
from rest_framework.request import Request
from rest_framework.serializers import BaseSerializer
from django.shortcuts import render
from rest_framework import viewsets
from .models import Task, Weather
from .serializers import TaskSerializer


from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework import generics

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.throttling import AnonRateThrottle
from rest_framework.exceptions import Throttled


class LoginRateThrottle(AnonRateThrottle):
    rate: str = '5/minute'


class ThrottledTokenObtainPairView(TokenObtainPairView):
    throttle_classes = [LoginRateThrottle]
    def throttled(self, request: Request | HttpRequest, wait: int) -> None:
        raise Throttled(detail="There were too many failed login attempts. Please try again later.")

class TaskViewSet(viewsets.ModelViewSet):
    # Tell Django which database data to pull
    queryset = Task.objects.all()
    
    # Tell Django which translator to use
    serializer_class = TaskSerializer

    def perform_create(self, serializer: BaseSerializer) -> None:
        serializer.save(owner=self.request.user)


def task_interface(request: HttpRequest) -> HttpResponse:
    latest_weather: Optional[Weather] = Weather.objects.first()
    weather_count: int = Weather.objects.count()
    
    diff: Optional[float] = None
    abs_diff: Optional[float] = None
    
    if weather_count > 1:
        # If we have at least 5 records, get the 5th (index 4)
        if weather_count >= 5:
            past_weather: Weather = Weather.objects.all()[4]
        # Otherwise, just grab the oldest available record
        else:
            past_weather: Weather = Weather.objects.last()
            
        diff = latest_weather.temp - past_weather.temp
        abs_diff = abs(diff)

    return render(request, "tasks.html", {"weather": latest_weather, "temp_diff": diff, "abs_diff": abs_diff})





class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
