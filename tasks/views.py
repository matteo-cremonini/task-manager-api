from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer

class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [AllowAny] # TODO: replace with IsAuthenticated

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [AllowAny] # TODO: replace with IsAuthenticated

    
    def get_queryset(self):
        queryset = Task.objects.filter(owner=self.request.user)
        status = self.request.query_params.get('status')
        project = self.request.query_params.get('project')
        completed = self.request.query_params.get('completed')
        is_working_on = self.request.query_params.get('is_working_on')

        if status:
            queryset = queryset.filter(status=status)
        if project:
            queryset = queryset.filter(project=project)
        if completed is not None:
            queryset = queryset.filter(completed=completed == 'true')
        if is_working_on is not None:
            queryset = queryset.filter(is_working_on=is_working_on == 'true')
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
