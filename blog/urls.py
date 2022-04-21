from django.urls import path
from . import views

urlpatterns = [
    path('blog/', views.blog, name='blog'),
    path('blog_detail/<int:pk>/', views.blog_detail, name='detail'),
]