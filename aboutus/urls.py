from django.urls import path
from . import views

urlpatterns = [
    path('aboutus/', views.about, name='about'),
    path('teams/', views.teams, name='teams'),
    path('clients/', views.client, name='clients'),
    path('contactus/', views.contactus, name='contact'),
    path('newsletter/', views.newsletter, name='newsletter'),

    #path('blog_detail/<int:pk>', views.blog_detail, name='detail'),
]