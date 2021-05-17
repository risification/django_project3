from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from .serializers import *
from rest_framework import viewsets
from rest_framework.views import APIView


# Create your views here.

class DossierModelViewSet(viewsets.ModelViewSet):
    queryset = Dossier.objects.all()
    serializer_class = DossierSerializers


# class DossierView(APIView):
#     def get(self, request, *args, **kwargs):
#         dossier = Dossier.objects.get(user=request.user)
#         serializers = DossierSerializers(dossier)
#         return Response(serializers.data)
#
#     def put(self, request, *args, **kwargs):
#         dossier = Dossier.objects.get(user=request.user)
#         serializers = DossierSerializers(dossier, data=request.data)
#         if serializers.is_valid():
#             serializers.save()
#             return Response({"Update successful!!!"})
#         return Response(serializers.errors)
#
#     def delete(self, request, *args, **kwargs):
#         dossier = Dossier.objects.get(user=request.user)
#         dossier.delete()
#         return Response({"data": "OK"})


class RegisterModelViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializers


class AuthView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})
