from django.urls import path, include
from .views import add, get

urlpatterns = [
    path('add/', add.CreateWorkspace.as_view()),
    path('is-owner/', get.GetOwnerWorkSpace.as_view()),
    path('is-member/', get.GetMemberWorkSpace.as_view()),

    path('member/', include('Member.urls')),
]
