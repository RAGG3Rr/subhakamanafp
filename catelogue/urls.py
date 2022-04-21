from django.urls import path
from . import views

urlpatterns = [
  path('catelogue/',views.catelogue, name="catelogue")
]
