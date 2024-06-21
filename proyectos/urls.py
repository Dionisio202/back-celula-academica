from django.urls import path
from . import views

urlpatterns = [
    path('register_proyecto/', views.register_proyecto, name='register_proyecto'),
    path('update_proyecto/<int:pk>/', views.update_proyecto, name='update_proyecto'),
    path('search_proyecto/', views.search_proyecto, name='search_proyecto'),
    path('delete_proyecto/', views.delete_proyecto, name='delete_proyecto'),
]