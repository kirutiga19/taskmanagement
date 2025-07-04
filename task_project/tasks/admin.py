from django.contrib import admin
from .models import Task
from .models import UserActivity


admin.site.register(Task)

@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'last_login_time', 'last_logout_time')
    readonly_fields = ('last_login_time', 'last_logout_time')
