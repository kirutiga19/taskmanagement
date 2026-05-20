from django.urls import path
from .views import register, login_view, my_tasks, update_task_status

urlpatterns = [
    path('register/', register),
    path('login/', login_view),
    path('my-tasks/', my_tasks),
    path('update-task/<int:task_id>/', update_task_status),
]
