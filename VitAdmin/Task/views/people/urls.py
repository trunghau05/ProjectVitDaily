from django.urls import path
from . import get, add, delete, update

urlpatterns = [
    path('add/', add.AddTaskPeople.as_view(), name='add-task-people'),
    path('delete/<str:ts_id>/', delete.DeleteTaskPeople.as_view(), name='delete-task-people'),
    path('update/<str:ts_id>/', update.UpdateTaskPeople.as_view(), name='update-task-people'),
    path("get/<str:tm_id>/", get.GetTask.as_view(), name="get-task-by-team"),
]
