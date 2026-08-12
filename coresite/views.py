# pyrefly: ignore [missing-import]
from typing import Optional, Any
from django.http import HttpRequest, HttpResponse
from rest_framework.request import Request
from rest_framework.serializers import BaseSerializer
from django.shortcuts import render
from rest_framework import viewsets
from .models import Project, Task, Weather
from .serializers import ProjectSerializer, TaskSerializer
from . import utils

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework import generics

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.throttling import AnonRateThrottle
from rest_framework.exceptions import Throttled

from schemas import TaskCreate, TaskCreateList



class LoginRateThrottle(AnonRateThrottle):
    rate: str = '5/minute'


class ThrottledTokenObtainPairView(TokenObtainPairView):
    throttle_classes = [LoginRateThrottle]
    def throttled(self, request: Request | HttpRequest, wait: int) -> None:
        raise Throttled(detail="There were too many failed login attempts. Please try again later.")

class TaskViewSet(viewsets.ModelViewSet):
    
    # Tell Django which translator to use
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)

    def perform_create(self, serializer: BaseSerializer) -> None:
        serializer.save(owner=self.request.user)


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
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



@api_view(['POST'])
def task_gen(request):
    if request.method == "POST":
        text: str = request.data.get("text")
        user_timezone: str = request.data.get("timezone", "UTC")
        if not text: 
            return Response({"message": "No text provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            tasks = utils.text_to_tasks(text, user_timezone)
        except Exception:
            tasks = utils.text_to_tasks(text, "UTC")

        for task in tasks:
            task_data = task.model_dump()
            new_task = Task.objects.create(owner=request.user, **task_data)
        return Response({"message": "Tasks created successfully"}, status=status.HTTP_201_CREATED)








class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer



