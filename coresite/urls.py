from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

# The router automatically generates all the URL paths for our ViewSet
router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('', include(router.urls)),
    path('interface/', task_interface, name='task-ui'),
    path("users/", UserList.as_view()),
    path("users/<int:pk>/", UserDetail.as_view()),
]