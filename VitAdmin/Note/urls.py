from django.urls import path
from .views import get, add, delete, filter, update

urlpatterns = [
    path('get_all_note/', get.NoteList.as_view(), name='note-list'),
    path('add/', add.AddNote, name='add-note'),
    path('delete/<str:nt_id>/', delete.DeleteNote, name='delete-note'),
    path('update/<str:nt_id>/', update.UpdateNote, name='update-note'),
]