from django.contrib import admin
from .models import Project, Task

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'timeline', 'owner', 'created_at']
    list_filter = ['timeline']

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'completed', 'is_working_on', 'project', 'owner']
    list_filter = ['status', 'completed', 'is_working_on']
