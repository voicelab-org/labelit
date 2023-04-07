from rest_framework import viewsets
from rest_framework import permissions
from labelit.serializers import (
    ProjectTaskSerializer,
)
from labelit.models import Batch, Project, ProjectTask
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Count
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from django.utils.translation import gettext as _
from django.utils.translation import activate
from django.http import HttpResponse, FileResponse
import os
import mimetypes
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend


class ProjectTaskFilter(filters.FilterSet):
    class Meta:
        model = ProjectTask
        fields = ["project"]


class ProjectTaskViewSet(viewsets.ModelViewSet):
    queryset = ProjectTask.objects.all()
    serializer_class = ProjectTaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProjectTaskFilter
