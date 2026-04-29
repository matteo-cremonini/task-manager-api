from django.db import models

from django.conf import settings

class Project(models.Model):
    TIMELINE_CHOICES = [
        ('undefined', 'To be defined'),
        ('short', 'Short-term'),
        ('medium', 'Medium-term'),
        ('long', 'Long-term'),
    ]
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    timeline = models.CharField(max_length=20, choices=TIMELINE_CHOICES)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
          on_delete=models.CASCADE,
          related_name='projects')
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.name
    
    def completion_percentage(self):
        tasks_total = self.tasks.count()
        tasks_completed = self.tasks.filter(completed=True).count()
        percentage = (tasks_completed / tasks_total) * 100 if tasks_total > 0 else 0
        return percentage
        

class Task(models.Model):
    STATUS_CHOICES = [
        ('undefined', 'Undefined'),
        ('today', 'Today'),
        ('this_week', 'This Week'),
        ('this_month', 'This Month'),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='undefined')
    completed = models.BooleanField(default=False)
    is_working_on = models.BooleanField(default=False)
    project = models.ForeignKey(
        Project, null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='tasks')
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.completed:
            self.is_working_on = False
        super().save(*args, **kwargs)


