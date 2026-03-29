# dashboard/urls.py
from django.urls import path
from .views import financial_dashboard

urlpatterns = [
    path('', financial_dashboard, name='financial_dashboard'),
]
