from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from .permission import *
from .serializers import *


# Create your views here.

class DocumentModelViewSet(viewsets.ModelViewSet):
    permission_classes = [FilterObjPermission]
    serializer_class = DocumentSerializers
    filter_backends = [SearchFilter]
    search_fields = ['status', 'document_root']

    def get_queryset(self):
        group = self.request.user.groups.all()[0].name
        if group == 'user':
            docs = Document.objects.filter(document_root__in=['public'])
        elif group == 'serjant':
            docs = Document.objects.filter(document_root__in=['public', 'private'])
        elif group == 'general':
            docs = Document.objects.filter(document_root__in=['public', 'private', 'secret'])
        elif group == 'president':
            docs = Document.objects.filter(document_root__in=['public', 'private', 'secret', 'top-secret'])
        return docs

