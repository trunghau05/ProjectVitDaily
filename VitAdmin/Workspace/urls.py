from django.urls import path, include
from .views import add, get, update, delete

urlpatterns = [
    path('add/', add.CreateWorkspace.as_view()),
    path('is-owner/', get.GetOwnerWorkSpace.as_view()),
    path('is-member/', get.GetMemberWorkSpace.as_view()),
    path('detail/', get.GetWorkSpaceDetail.as_view()),
    path('update/', update.UpdateWorkSpace.as_view()),
    path('delete/<str:ws_id>/', delete.DeleteWorkSpace.as_view()),

    path('member/', include('Member.urls')),
]
