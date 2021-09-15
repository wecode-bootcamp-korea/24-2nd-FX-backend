from django.urls import path

from .views import ContentView, ContentListView

urlpatterns = [
    path("/<int:content_id>", ContentView.as_view()),
    path("/list", ContentListView.as_view()),
]