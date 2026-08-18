from rest_framework import serializers
from .models import Task, Weather, Project
from django.contrib.auth.models import User


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        # '__all__' tells Django to automatically translate every column we made in the database
        fields = '__all__'
        read_only_fields = ['owner'] 

class ProjectSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)
    github_token = serializers.CharField(
        write_only=True, required=False, allow_blank=True, default=""
    )

    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ["owner", "ast_outline"]


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


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate_username(self, value: str) -> str:
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with that username already exists.")
        return value

    def validate_email(self, value: str) -> str:
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("An account with this email already exists.")
        return value

    def create(self, validated_data: dict) -> User:
        return User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )

