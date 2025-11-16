from django.urls import path
from .views import get, add, delete, update

urlpatterns = [
    path('<str:ts_id>/add/', add.AddSubtask.as_view(), name="add-subtask"),
    path('<str:ts_id>/get/', get.ListSubtasks.as_view(), name="list-subtask"),
    path('<str:ts_id>/<str:st_id>/update/', update.UpdateSubtask.as_view(), name="update-subtask"),
    path('<str:ts_id>/<str:st_id>/delete/', delete.DeleteSubtask.as_view(), name="delete-subtask"),
]

