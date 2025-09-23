from django.urls import path
from . import views

urlpatterns = [
    path('', views.ai_view, name='ai_view'),
]
