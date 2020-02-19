from .serializers import AuthorSerializer, DocumentSerializer
from rest_framework.parsers import JSONParser
from .models import Document, Author
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def document_list(request):
    if request.method == 'GET':
        objs = Document.objects.all()
        serializer = DocumentSerializer(objs, many=True)
        return JsonResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = DocumentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def document_detail(request, pk):
    try:
        obj = Document.objects.get(pk=pk)
    except Document.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = DocumentSerializer(obj)
        return JsonResponse(serializer.data)
    if request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = DocumentSerializer(obj, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    if request.method == 'DELETE':
        obj.delete()
        return HttpResponse(status=204)



########################################################################################################################


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Document
from .serializers import DocumentSerializer


@api_view(['GET', 'POST'])
def document_list(request):
    if request.method == 'GET':
        objs = Document.objects.all()
        serializer = DocumentSerializer(objs, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = DocumentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def document_detail(request, pk):
    try:
        obj = Document.objects.get(pk=pk)
    except Document.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DocumentSerializer(obj)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = DocumentSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


from django.urls import path
from . import views

urlpatterns = [
    path('document/', document_list),
    path('document/<int:pk>', document_detail)
]

########################################################################################################################


from .models import Document
from .serializers import DocumentSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404


class DocumentList(APIView):
    def get(self, request):
        objs = Document.objects.all()
        serializer = DocumentSerializer(objs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DocumentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DocumentDetail(APIView):
    def get_object(self, pk):
        try:
            return Document.objects.get(pk=pk)
        except Document.DoesNotExist:
            return Http404

    def patch(self, request, pk):
        obj = self.get_object(pk)
        serializer = DocumentSerializer(obj)
        return Response(serializer.data)

    def put(self, request, pk):
        obj = self.get_object(pk)
        serializer = DocumentSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        obj = self.get_object(pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

urlpatterns = [
    path('documents/', DocumentList.as_view()),
    path('documents/<int:pk>/', DocumentDetail.as_view())
]

########################################################################################################################

from rest_framework import generics
from rest_framework import mixins


class DocumentList(generics.GenericAPIView,
                   mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class DocumentDetail(generics.GenericAPIView,
                     mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

########################################################################################################################


class DocumentList(generics.ListCreateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer


class DocumentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer





