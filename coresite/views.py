# pyrefly: ignore [missing-import]
from requests import packages
from requests import packages
from rest_framework import viewsets
from .models import Task, Weather
from .serializers import TaskSerializer
# pyrefly: ignore [missing-import]
from django.shortcuts import render, redirect
# pyrefly: ignore [missing-import]
from django.core.cache import cache

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404


class TaskViewSet(viewsets.ModelViewSet):
    # Tell Django which database data to pull
    queryset = Task.objects.all()
    
    # Tell Django which translator to use
    serializer_class = TaskSerializer



def delete_task_html(request, task_id):
    # Securely check that it's a POST request before deleting
    if request.method == 'POST':
        try:
            task = Task.objects.get(id=task_id)
            task.delete()  # This will also trigger your signal alarm!
            cache.delete("todo_list_cache")
            print(f"🗑️ CACHE WIPED: Task {task_id} deleted from database!", flush=True)
        except Task.DoesNotExist:
            pass
    return redirect('task-ui')  # Refresh the page







def task_list_html(request):
    # 1. HERE IS THE INTERCEPTOR: If the user clicked "Add Task"
    if request.method == "POST":
        title = request.POST.get("title")
        if title:
            # Physically save it to the database inside the container
            Task.objects.create(title=title)
            
            # Blow up the stale cache so the new item shows up instantly
            cache.delete("todo_list_cache") 
            print("🗑️ CACHE WIPED: New item saved to database!", flush=True)
            
        return redirect(request.path) # Reload the page cleanly

    # 2. THE GET LOGIC: If the user is just looking at the page
    cached_tasks = cache.get("todo_list_cache")
    
    if cached_tasks is not None:
        print("🚀 FETCHED FROM REDIS CACHE!", flush=True)
        tasks = cached_tasks
    else:
        print("🐢 CACHE MISS! Fetching fresh data from database...", flush=True)
        tasks = list(Task.objects.all())
        cache.set("todo_list_cache", tasks, timeout=60)
        
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

    return render(request, "tasks.html", {"tasks": tasks, "weather": latest_weather, "temp_diff": diff, "abs_diff": abs_diff})

def get_weather_category(weather_code: int) -> str:
    """
    Maps an Open-Meteo (WMO) weather code to its official string description.
    
    Args:
        weather_code (int): The numeric weather code.
        
    Returns:
        str: A string describing the weather condition.
    """
    wmo_codes = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Drizzle: Light intensity",
        53: "Drizzle: Moderate intensity",
        55: "Drizzle: Dense intensity",
        56: "Freezing Drizzle: Light intensity",
        57: "Freezing Drizzle: Dense intensity",
        61: "Rain: Slight intensity",
        63: "Rain: Moderate intensity",
        65: "Rain: Heavy intensity",
        66: "Freezing Rain: Light intensity",
        67: "Freezing Rain: Heavy intensity",
        71: "Snow fall: Slight intensity",
        73: "Snow fall: Moderate intensity",
        75: "Snow fall: Heavy intensity",
        77: "Snow grains",
        80: "Rain showers: Slight",
        81: "Rain showers: Moderate",
        82: "Rain showers: Violent",
        85: "Snow showers: Slight",
        86: "Snow showers: Heavy",
        95: "Thunderstorm: Slight or moderate",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail"
    }
    
    # Return the description, or a default message if the code isn't recognized
    return wmo_codes.get(weather_code, "Unknown weather code")



#API ENDPOINTS

@api_view(['POST'])
def create_task_api(request):
    serialiser = TaskSerializer(data=request.data)

    if(serialiser.is_valid()):
        serialiser.save()
        return Response(serialiser.data, status=status.HTTP_201_CREATED)
    
    return Response(serialiser.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
def read_task_api(request,task_id):

    task = get_object_or_404(Task,id=task_id)
    serializer = TaskSerializer(task)
    return Response(serializer.data)

@api_view(['GET'])
def read_task_all_api(request):
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['PUT'])
def update_task_api(request,task_id):

    task = get_object_or_404(Task,id=task_id)
    serialiser = TaskSerializer(task, data=request.data, partial= True)

    if serialiser.is_valid():
        serialiser.save()
        return Response(serialiser.data)
    return Response(serialiser.errors, status=400)


@api_view(['DELETE'])
def delete_task_api(request,task_id):
    task = get_object_or_404(Task,id=task_id)
    task.delete()

    return Response(
        {"message": "Task deleted successfully!"}, 
        status=status.HTTP_204_NO_CONTENT
    )