from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Genus
from .serializers import GenusSerializer

class GenusViews():
    @api_view(['GET', 'POST'])
    def genus_list(request):
        if request.method == 'GET':
            genuses = Genus.objects.all()
            serializer = GenusSerializer(genuses, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
            serializer = GenusSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'PUT':
            serializer = GenusSerializer(Genus, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @api_view(['GET','PUT','DELETE'])
    def genus_detail(request, pk):
        try:
            genus = Genus.objects.get(pk=pk)
        except Genus.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = GenusSerializer(genus)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = GenusSerializer(genus, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            genus.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
