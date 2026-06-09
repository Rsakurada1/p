from django.urls import path

from .views import (
    LoginView,
    LogoutView,
    MeView,
    RegisterView,
    TaskDetailView,
    TaskListCreateView,
    health_check,
)

urlpatterns = [
    path('health/', health_check, name='health-check'),
    path('auth/register/', RegisterView.as_view(), name='auth-register'),
    path('auth/login/', LoginView.as_view(), name='auth-login'),
    path('auth/logout/', LogoutView.as_view(), name='auth-logout'),
    path('auth/me/', MeView.as_view(), name='auth-me'),
    path('tasks/', TaskListCreateView.as_view(), name='task-list'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
]
