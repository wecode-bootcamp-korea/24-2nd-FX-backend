from django.urls import path

from .views import ContentView

urlpatterns = [
    path("/<int:content_id>", ContentView.as_view()),
]