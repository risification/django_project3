from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('dossier', DossierModelViewSet)
router.register('register', RegisterModelViewSet)
urlpatterns = [
    path('', include(router.urls)),
]
