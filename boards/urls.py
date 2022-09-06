from django.urls import path

from . import views

urlpatterns = [
    path("get_board_list/", views.get_board_list),
    path("get_board_detail/<int:id>/", views.get_board_detail),
]
