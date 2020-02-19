from rest_framework import parsers, decorators
from rest_framework import response
from rest_framework import status
from rest_framework import viewsets

from .models import Document, Author
from .serializers import DocumentSerializer, DocumentImageSerializer, AuthorSerializer


class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer
    queryset = Document.objects.all()

    @decorators.action(
        detail=True,
        methods=['PUT'],
        serializer_class=DocumentImageSerializer,
        parser_classes=[parsers.MultiPartParser],
    )
    def pic(self, request, pk):
        obj = self.get_object()
        serializer = self.serializer_class(obj, data=request.data,
                                           partial=True)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
        return response.Response(serializer.errors,
                                 status.HTTP_400_BAD_REQUEST)


class AuthorViewSet(viewsets.ModelViewSet):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()


