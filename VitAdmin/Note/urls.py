from django.urls import path
from .views import get, add, delete, filter, update

urlpatterns = [
    path('getList/', get.NoteList.as_view(), name='note-list'),
]