from django.urls import path
from .views import get, add, update, delete

urlpatterns = [
    path('get/<str:ws_id>/', get.GetMembersByWorkspace.as_view()),
    path('add/', add.AddMembers.as_view()),
    path('add-to-team/', add.AddMemberToTeam.as_view()),
    path('update/<str:ws_id>/<str:us_id>/', update.UpdateMemberInWorkspace.as_view()),
    path('delete/<str:ws_id>/<str:us_id>/', delete.RemoveMemberFromWorkspace.as_view()),
]
