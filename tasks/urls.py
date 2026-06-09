from django.urls import path

from .views import health_check, task_list

urlpatterns = [
    path("health/", health_check),
    path("tasks/", task_list),
]
