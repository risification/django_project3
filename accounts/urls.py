from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('dossiers', DossierModelViewSet)
router.register('register', RegisterModelViewSet)
urlpatterns = [
    path('', include(router.urls), name='start'),
    path('login/', AuthView.as_view(), name='login'),
    # path('dossier_delete/', DossierView.as_view())
]
