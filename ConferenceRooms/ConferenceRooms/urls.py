"""ConferenceRooms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ConferenceRooms_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('overview/', views.Overview.as_view(), name='all_rooms'),
    path('room/new/', views.AddNewRoom.as_view(), name='add_room'),
    path('room/<int:room_id>', views.RoomDetails.as_view()),
    path('room/reserve/<int:room_id>', views.RoomBooking.as_view()),
    path('room/delete/', views.delete_room),
    path('room/delete/<int:room_id>/', views.DeleteRoom.as_view(), name='delete_room'),
    path('room/modify/', views.modify_room),
    path('room/modify/<int:room_id>', views.ModifyRoom.as_view(), name='modify_room'),

]
