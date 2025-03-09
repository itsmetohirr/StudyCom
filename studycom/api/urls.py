from django.urls import path
from . import views


urlpatterns = [
    path('', views.get_routes),
    path('rooms/', views.get_rooms),
    path('room-detail/<int:pk>', views.get_room_detail)
]
