from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

# The router automatically generates all the URL paths for our ViewSet
router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('', include(router.urls)),
    path('interface/', task_list_html, name='task-ui'),
    path('interface/delete/<int:task_id>/', delete_task_html, name='delete-task-ui'),


    path('endpoints/create/', create_task_api, name='create_task_api'),
    path('endpoints/tasks/', read_task_all_api, name='read_task_all_api'),
    path('endpoints/tasks/<int:task_id>/', read_task_api, name='read_task_api'),
    path('endpoints/update/<int:task_id>/', update_task_api, name='update_task_api'),
    path('endpoints/delete/<int:task_id>/', delete_task_api, name='delete_task_api'),

]