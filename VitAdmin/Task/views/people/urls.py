from django.urls import path
from . import get, add, delete, update

urlpatterns = [
    path('addtask/', add.AddTaskPeople.as_view(), name='add-task-people'),
    path('deletetask/<str:ts_id>/', delete.DeleteTaskPeople.as_view(), name='delete-task-people'),
    path('updatetask/<str:ts_id>/', update.UpdateTaskPeople.as_view(), name='update-task-people'),
    path("get/<str:tm_id>/", get.GetTask.as_view(), name="get-task-by-team"),
]