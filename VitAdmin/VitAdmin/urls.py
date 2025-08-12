from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('User.urls')),
    path('tasks/', include('Task.urls')),
    path('notes/', include('Note.urls')), 
]
