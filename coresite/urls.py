from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

# The router automatically generates all the URL paths for our ViewSet
router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'projects', ProjectViewSet, basename='project')

urlpatterns = [
    path("tasks/gen/", task_gen, name="task-gen"),
    path('', include(router.urls)),
    path('interface/', task_interface, name='task-ui'),
    path("users/", UserList.as_view()),
    path("users/<int:pk>/", UserDetail.as_view()),
]