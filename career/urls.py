from django.urls import path
from . import views

urlpatterns = [
    path('career/', views.vacancy, name='vacancy'),
    path('vacancydetail/<slug:slug>', views.vacancydetail, name='vacancydetail'),
    path('job-apply/<slug:slug>', views.jobapply, name='jobapply'),

]