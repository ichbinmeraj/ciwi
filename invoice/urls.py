from django.urls import path
from . import views

urlpatterns = [
    path("workshop/", views.workshop, name="workshop"),
    path("mechanickala/", views.mechanickala, name="mechanickala"),
    
    path("lists/<str:page>/", views.lists, name="lists"),
    path("create/<str:page>/", views.create, name="create"),
    path("update/<str:page>/<int:id>", views.details, name="create"),

    path("create_invoice/<str:page>/", views.create_invoice, name="create_invoice"),
    path("print_invoice/<str:page>/<int:id>/", views.print_invoice, name="print_invoice"),
    path('deactivate/<int:id>', views.deactive_invoice, name='deactivate_invoice'),
    path('deactivate/<str:page>/<int:id>', views.deactive, name='deactive'),
]