from django.urls import path
from .views import get, add, delete, filter, update

urlpatterns = [
    path('note-list/', get.NoteList.as_view(), name='note-list'),
    path('detail/', get.NoteDetail.as_view(), name='note-detail'),
    path('add/', add.AddNote, name='add-note'),
    path('delete/<str:nt_id>/', delete.DeleteNote, name='delete-note'),
    path('update/<str:nt_id>/', update.UpdateNote, name='update-note'),
]