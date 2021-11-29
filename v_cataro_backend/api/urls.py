from .views import generate_response, check_emotion
from django.urls import path

urlpatterns = [
    path("answer", generate_response),
    path("emotion", check_emotion),
]