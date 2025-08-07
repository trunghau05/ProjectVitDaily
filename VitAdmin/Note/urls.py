from django.urls import path
from .views import get

urlpatterns = [
    path('getList/', get.NoteList.as_view(), name='note-list'),
]