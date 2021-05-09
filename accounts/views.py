from django.shortcuts import render
from rest_framework.response import Response
from .serializers import *
from rest_framework import viewsets


# Create your views here.

class DossierModelViewSet(viewsets.ModelViewSet):
    queryset = Dossier.objects.all()
    serializer_class = DossierSerializers


class RegisterModelViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializers
