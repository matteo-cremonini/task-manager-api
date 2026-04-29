from tasks.models import Project, Task
from rest_framework import serializers


class TaskSerializer(serializers.ModelSerializer):
    project_name = serializers.StringRelatedField(source='project')
    
    
    class Meta:
        model = Task
        fields = [ 'id', 'title', 'description', 'project', 'status', 'is_working_on','completed', 'project_name', 'owner', 'created_at', 'updated_at']
        read_only_fields = ['owner','created_at', 'updated_at']


class ProjectSerializer(serializers.ModelSerializer):
    completion_percentage = serializers.SerializerMethodField()
    tasks = TaskSerializer(many=True, read_only=True)
    
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'timeline', 'tasks', 'completion_percentage', 'owner', 'created_at',]
        read_only_fields = ['owner','created_at',]

    def get_completion_percentage(self, obj):
        return obj.completion_percentage()