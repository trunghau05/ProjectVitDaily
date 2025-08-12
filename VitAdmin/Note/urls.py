from django.urls import path
from .views import get, add, delete, filter, update

urlpatterns = [
    path('getList/', get.NoteList.as_view(), name='note-list'),
    path('add/', add.add_note, name='add-note'),
    path('delete/<str:nt_id>/', delete.delete_note, name='delete-note'),
    path('update/<str:nt_id>/', update.update_note, name='update-note'),
]