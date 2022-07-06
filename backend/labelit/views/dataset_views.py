import imp
from rest_framework import viewsets
from rest_framework import permissions
from labelit.serializers import DatasetSerializer
from labelit.models import Dataset, DocumentSequence, Document
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
import pandas as pd
import distutils
from rest_framework.parsers import MultiPartParser
from rest_framework.exceptions import ParseError, ValidationError
from rest_framework import status


class DatasetViewSet(viewsets.ModelViewSet):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]


class DatasetUploadAPI(APIView):
    parser_classes = (MultiPartParser,)
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def post(self, request):
        if 'file' not in request.data:
            raise ParseError('Empty content')

        self.create_dataset(
            file=request.data['file'],
            dataset_name=request.data['dataset_name'],
            is_streamed=distutils.util.strtobool(request.data['is_streamed']),
        )

        return Response({'status': 'created'}, status=status.HTTP_201_CREATED)

    @classmethod
    def create_dataset(cls, file, dataset_name ,is_streamed):
        data = pd.read_csv(file)
        if not all(c in data.columns for c in ['text', 'basename', 'duration', 'seq_index', 'audio_filename']):
            raise ValidationError(
                'file must be in csv format and contains those columns (text,basename,duration,seq_index,audio_filename)')

        dataset, dataset_created = Dataset.objects.get_or_create(
            name=dataset_name)
        cls.create_docs(data, dataset)
        Dataset.objects.filter(id=dataset).update(is_streamed=is_streamed)

    @classmethod
    def create_docs(cls, docs_data, dataset):
        known_doc_seq = set()
        docs_seq = {}
        for index, row in docs_data.iterrows():
            filename = row["basename"]
            if filename not in known_doc_seq:
                known_doc_seq.add(filename)
                docs_seq[filename] = []
            docs_seq[filename].append(
                {
                    "document_index": row["seq_index"],
                    "duration": row["duration"],
                    "text": row["text"],
                    "audio_filename": row["audio_filename"],
                }
            )
        for doc_seq_name in docs_seq:
            document_sequence, created = DocumentSequence.objects.get_or_create(
                name=doc_seq_name, dataset=dataset
            )
            docs = sorted(docs_seq[doc_seq_name],
                          key=lambda k: k["document_index"])
            for i, doc in enumerate(docs):
                _doc = Document.objects.filter(
                    audio_filename=doc["audio_filename"], dataset=dataset)
                if not _doc.count():
                    Document.objects.create(
                        text=doc["text"],
                        audio_filename=doc["audio_filename"],
                        sequence_index=i,
                        document_sequence=document_sequence,
                        dataset=dataset,
                        audio_duration=doc["duration"]
                    )
                else:
                    print('docs already exist')
