from django.urls import path
from . import views

urlpatterns = [
    path('privacypolicies/', views.policy, name='policy'),
    path('exchange/', views.exchange, name='exchange'),
]