from rest_framework import viewsets
from rest_framework import permissions
from labelit.serializers import TaskPolymorphicSerializer
from labelit.models import Task, Batch, Project
from rest_framework.decorators import action
from rest_framework.response import Response


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskPolymorphicSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, name='Get agreement metrics over batch')
    def get_agreement_stats_for_batch(self, request, pk=None):
        task = Task.objects.get(pk=pk)
        batch_id = self.request.query_params.get('batch_id', None)
        batch = Batch.objects.get(
            pk=batch_id
        )
        return Response(
            task.get_agreement_stats(batch)
        )

    @action(detail=True, name='Get task-specific stats for this batch')
    def get_batch_stats(self, request, pk=None):
        task = Task.objects.get(pk=pk)
        batch_id = self.request.query_params.get('batch_id', None)
        batch = Batch.objects.get(
            pk=batch_id
        )
        stats = task.get_batch_stats(batch)
        return Response(
            stats
        )
    
    @action(detail=True, name='Get task-specific stats for this project')
    def get_project_stats(self, request, pk=None):
        task = Task.objects.get(pk=pk)
        project_id = self.request.query_params.get('project_id', None)
        project = Project.objects.get(
            pk=project_id
        )
        stats = task.get_project_stats(project)
        return Response(
            stats
        )

    def list(self, request):
        if request.query_params.get('project_id', None):
            queryset = Task.objects.filter(project_id=request.query_params.get('project_id', None))
        else:
            queryset = Task.objects.all()
        serializer = TaskPolymorphicSerializer(queryset, many=True)
        return Response(serializer.data)
