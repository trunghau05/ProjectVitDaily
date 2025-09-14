from django.urls import path
from .views import get, add, delete, update

urlpatterns = [
    path('add/', add.AddTask, name='add-task'),
    path('update/<str:ts_id>/', update.UpdateTask, name='update-task'),
    path('delete/<str:ts_id>/', delete.DeleteTask, name='delete-task'),
]