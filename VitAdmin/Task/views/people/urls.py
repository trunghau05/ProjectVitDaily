from django.urls import path
from . import get, add, delete, update

urlpatterns = [
    path('add/', add.AddTaskPeople.as_view(), name='add-task-people'),
    path('delete/<str:ts_id>/', delete.DeleteTaskPeople.as_view(), name='delete-task-people'),
    path('update/<str:ts_id>/', update.UpdateTask.as_view(), name='update-task-people'),
    path("get/<str:tm_id>/", get.GetTaskByTeam.as_view(), name="get-task-by-team"),
    path('detail/<str:ts_id>', get.GetTaskDetail.as_view()),
]
