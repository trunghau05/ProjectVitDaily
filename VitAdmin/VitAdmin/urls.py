from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('User.urls')),
    path('task/', include('Task.urls')),
    path('note/', include('Note.urls')), 
    path('vitai/', include('VitAi.urls')),
    path('workspace/', include('Workspace.urls')),
]
