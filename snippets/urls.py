from django.urls import path, include
from rest_framework import routers
from .views import AuthorViewSet, DocumentViewSet
router = routers.DefaultRouter()

router.register(r'documents', DocumentViewSet)
router.register(r'author', AuthorViewSet)

urlpatterns = [
    path(r'api/v1/', include(router.urls)),
]
