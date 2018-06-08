
from django.urls import path

from commom import views

urlpatterns = [
    path('', views.index)
]