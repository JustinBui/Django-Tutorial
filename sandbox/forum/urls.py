from . import views
from django.urls import path


urlpatterns = [
    path('login_register/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_page, name='register'),
    path('', views.home, name='home'),
    # path('topics/<str:pk>/', views.topics, name='topic'),
    path('topics/<str:pk>/', views.topics, name='topic'),
    path('create-topic/', views.create_topic, name='create-topic'),
    path('update-topic/<str:pk>/', views.update_topic, name='update-topic'),
    path('delete-topic/<str:pk>/', views.delete_topic, name='delete-topic'),
]