from django.urls import path
from .views import get, add, update, delete

urlpatterns = [
    path('get/', get.GetTeamByWorkspace.as_view()),
    path('add/', add.CreateTeam.as_view()),
    path('detail/', get.GetTeamDetail.as_view()),
    path('update/<str:tm_id>', update.UpdateTeam.as_view()),
    path('delete/<str:tm_id>', delete.DeleteTeam.as_view())
]
