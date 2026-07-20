from rest_framework import serializers
from .models import Task, Weather


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        # '__all__' tells Django to automatically translate every column we made in the database
        fields = '__all__'


class WeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weather
        fields = '__all__'