from rest_framework import serializers
from .models import Author, Document


class DocumentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Document
        fields = ['id', 'title', 'author', 'image']
        read_only_fields = ('author', )
        depth = 1


class DocumentImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['image']


class AuthorSerializer(serializers.ModelSerializer):
    doc = DocumentSerializer(many=True)

    class Meta:
        model = Author
        fields = ['first_name', 'last_name', 'description', 'doc']














