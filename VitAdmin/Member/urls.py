from django.urls import path
from .views import get, add

urlpatterns = [
    path('get/<str:ws_id>/', get.GetMembersByWorkspace.as_view()),
    path('add/', add.AddMember.as_view()),
]
