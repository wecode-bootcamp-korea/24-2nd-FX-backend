from django.urls import path

from .views import ContentView, ContentListView, ContentStreamingView

urlpatterns = [
    path("/<int:content_id>", ContentView.as_view()),
    path("/list", ContentListView.as_view()),
    path("/streaming/<int:detail_id>", ContentStreamingView.as_view()),
]