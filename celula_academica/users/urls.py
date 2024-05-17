from django.urls import path
from . import views

urlpatterns=[
     path('login/', views.login),
     path('register/', views.register),
     path('profile/', views.profile),
     path('update_user/', views.update_user),
    path('search_user/', views.search_user),
]