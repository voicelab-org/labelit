from rest_framework import viewsets, permissions, exceptions
from rest_framework.response import Response
from rest_framework.decorators import action

from labelit.serializers import ProjectSerializer, ProjectWithStatsSerializer, ExportedProjectSerializer
from labelit.models import Project, Dataset, Document, Batch, SequenceBatch


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, name='Get progress stats for the batch')
    def get_remaining_units_in_dataset(self, request, pk=None):
        project = Project.objects.get(id=pk)
        try:
            dataset_id = request.query_params.get('dataset_id', None)
            dataset = Dataset.objects.get(pk=dataset_id)
        except Dataset.DoesNotExist as exc:
            exc = exceptions.NotFound()
            data = {'detail': exc.detail}
            return Response(data, exc.status_code)
        
        if project.are_sequences_annotated:
            batch_class = SequenceBatch
        else:
            batch_class = Batch

        num_units = batch_class.get_remaining_units_in_dataset(project, dataset)
        data = {
            'count': num_units
        }
        return Response(data)

    @action(detail=True, name='Get annotation stats for this batch')
    def get_stats(self, request, pk=None):
        project = Project.objects.get(pk=pk)
        return Response(project.get_stats())



class ProjectWithStatsViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectWithStatsSerializer
    permission_classes = [permissions.IsAuthenticated]


from django.http import FileResponse
from rest_framework import viewsets, renderers
from rest_framework.decorators import action
import os
import json

class PassthroughRenderer(renderers.BaseRenderer):
    """
        Return data as-is. View should supply a Response.
    """
    media_type = ''
    format = ''
    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data


class ProjectExportViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ExportedProjectSerializer
    permission_classes = [permissions.IsAuthenticated]


    @action(detail=True, name='Get export file (.json)')
    def download(self, request, pk=None):

        # with open('./dummy.txt', 'w') as f:
        #    f.write('TOY')

        # size = os.path.getsize('./dummy.txt')
        # file_handle = open('./dummy.pdf', 'rb')
        # send file
        """
        response = FileResponse(file_handle, content_type='text/plain')
        response['Content-Length'] = size
        response['Content-Disposition'] = 'attachment; filename="dummy.txt"'
        """
        # response = FileResponse(file_handle, as_attachment=True)
        # response["Access-Control-Allow-Origin"] = "http://localhost:8081"  # HACK
        # response['Content-Disposition'] = 'attachment; filename=dummy.txt'

        project = Project.objects.get(pk=pk)
        serializer = self.get_serializer(project, many=False)

        with open('./export.json', 'w') as file_handle:
            json.dump(serializer.data, file_handle)

        file_handle = open('./export.json', 'rb')

        response = FileResponse(file_handle, as_attachment=True)
        # response["Access-Control-Allow-Origin"] = "http://localhost:8081"  # HACK
        # response['Content-Disposition'] = 'attachment; filename=dummy.txt'

        return response


