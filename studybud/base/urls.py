# URLS file for this specific app (NOTE: WE must make this file upon creating new app directories)

from django.urls import path
from . import views # From the current durectory of where urls is


urlpatterns = [
    # First parameter: Getting the path at home directory (by default '')
    # Second parameter: getting the home() funcion from the views file
    # Third parameter: Name it 'home' to referencce it by its name later
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),
    path('', views.home, name='home'),
    path('room/<str:pk>/', views.room, name='room'), # Using dynamic URL's, where pk is a string parameter (See function in views.py)
    path('create-room/', views.createRoom, name='create-room'),
    path('update-room/<str:pk>/', views.updateRoom, name='update-room'),
    path('delete-room/<str:pk>/', views.deleteRoom, name='delete-room'),
    path('delete-message/<str:pk>/', views.deleteMessage, name='delete-message'),
]