from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class Task(models.Model):
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('start', 'Start'),
        ('on_process', 'On Process'),
        ('completed', 'Completed'),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    assignee = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    
class UserActivity(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    last_login_time = models.DateTimeField(null=True, blank=True)
    last_logout_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} Activity"
