from django.urls import path
from . import views

urlpatterns = [
    path("workshop/", views.workshop, name="workshop"),
    path("mechanickala/", views.mechanickala, name="mechanickala")
]