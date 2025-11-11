from django.urls import path
from . import get, add, delete, update

urlpatterns = [
    path('task-list/', get.TaskList, name='task-list'),
    path('task-detail/', get.TaskDetail, name='task-detail'),
    path('add/', add.AddTask, name='add-task'),
    path('update/<str:ts_id>/', update.UpdateTask, name='update-task'),
    path('delete/<str:ts_id>/', delete.DeleteTask, name='delete-task'),
]