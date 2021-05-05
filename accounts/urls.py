from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('dossier', DossierModelViewSet)
router.register('register', RegisterModelViewSet)
router.register('education', EducationModelViewSet)
router.register('warcraft', WarcraftModelViewSet)
router.register('car', CarModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
