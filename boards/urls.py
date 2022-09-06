from django.urls import path

from .views import BoardAPI, BoardsAPI

urlpatterns = [
    path("", BoardsAPI.as_view()),
    path("/<int:id>", BoardAPI.as_view()),
    path("", BoardsAPI.as_view()),
    path("/<int:id>", BoardAPI.as_view()),
]
