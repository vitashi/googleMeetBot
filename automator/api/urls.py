from django.urls import path

from .views import Index, API, Updates

urlpatterns = [
    path('', Index.as_view()),
    path('bot/', API.as_view()),
    path('updates/<str:sessionID>/', Updates.as_view())
]