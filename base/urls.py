from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('room/<str:pk>', views.room, name='room'),
    
    path('create-room', views.createRoom, name='create-room'),
    path('update-room/<str:pk>', views.update_room, name='update-room'),
    path('delete-room/<str:pk>', views.delete_room, name='delete-room'),
    path('delete-message/<str:pk>', views.deleteMessage, name='delete-message'),
    
    path('register', views.register, name='register'),
    
    path('login/', views.loginuser, name='login'),
    path('logout', views.logoutuser, name='logout'),
    path('user-profile/str:pk>/', views.userprofile, name='user-profile'),
  
  
    
]

