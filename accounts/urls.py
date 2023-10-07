from django.urls import path

from .views import SignUpView, CustomLogInView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', CustomLogInView.as_view(), name='login')
]