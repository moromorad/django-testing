# pyrefly: ignore [missing-import]
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
    rate = '5/minute'


class ThrottledTokenObtainPairView(TokenObtainPairView):
    throttle_classes = [LoginRateThrottle]
    def throttled(self, request, wait):
        raise Throttled(detail="There were too many failed login attempts. Please try again later.")

class TaskViewSet(viewsets.ModelViewSet):
    # Tell Django which database data to pull
    queryset = Task.objects.all()
    
    # Tell Django which translator to use
    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


def task_interface(request):
    latest_weather = Weather.objects.first()
    weather_count = Weather.objects.count()
    
    diff = None
    if weather_count > 1:
        # If we have at least 5 records, get the 5th (index 4)
        if weather_count >= 5:
            past_weather = Weather.objects.all()[4]
        # Otherwise, just grab the oldest available record
        else:
            past_weather = Weather.objects.last()
            
        diff = latest_weather.temp - past_weather.temp
        abs_diff = abs(diff)
    else:
        abs_diff = None

    return render(request, "tasks.html", {"weather": latest_weather, "temp_diff": diff, "abs_diff": abs_diff})





class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
