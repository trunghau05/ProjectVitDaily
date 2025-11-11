from django.urls import path, include

urlpatterns = [
    path('person/', include('Task.views.person.urls')),
    path('people/', include('Task.views.people.urls')),
]