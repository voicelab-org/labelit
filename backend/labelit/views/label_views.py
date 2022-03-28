from rest_framework import viewsets
from rest_framework import permissions
from labelit.serializers import LabelPolymorphicSerializer, LabelPolymorphicReadSerializer
from labelit.models import Label


class LabelViewSet(viewsets.ModelViewSet):
    queryset = Label.objects.all()
    # serializer_class = LabelPolymorphicSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        # create, retrieve
        if self.action == "create" or self.action == "update":
            return LabelPolymorphicSerializer
        return LabelPolymorphicReadSerializer
