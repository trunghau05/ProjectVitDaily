from django.urls import path
from .views import get, login, register

urlpatterns = [
    path('get_user_by_id/<str:us_id>/', get.get_user_by_id, name='get_user_by_id'),
]