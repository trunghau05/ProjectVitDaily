from django.urls import path
from .views import add

urlpatterns = [
    path('add/', add.InsertSampleData.as_view()),
]
