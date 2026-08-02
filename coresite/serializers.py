from rest_framework import serializers
from .models import Task, Weather
from django.contrib.auth.models import User


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        # '__all__' tells Django to automatically translate every column we made in the database
        fields = '__all__'


class WeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weather
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):

    tasks = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Task.objects.all()
    )

    class Meta:
        model = User
        fields = ["id", "username", "tasks", "owner"]

    owner = serializers.ReadOnlyField(source="owner.username")

