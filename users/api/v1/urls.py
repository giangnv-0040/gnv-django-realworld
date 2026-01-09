from django.urls import path
from .views import LoginView, RegisterView, GetCurrentUserView

urlpatterns = [
    path('users/login', LoginView.as_view(), name='login'),
    path('users', RegisterView.as_view(), name='register'),
    path('user', GetCurrentUserView.as_view(), name='user'),  # Handles both GET and PUT
]
