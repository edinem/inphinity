from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from ..models import PPISource
from ..serializers import PPISourceSerializer
from ..permissions import *

class PPISourceView():
    @api_view(['GET', 'POST'])
    @permission_classes([OnlyRead, ])
    def ppiSource_list(request):
        if request.method == 'GET':
            ppiSources = PPISource.objects.all()
            serializer = PPISourceSerializer(ppiSources, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
            serializer = PPISourceSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET','PUT','DELETE'])
    @permission_classes([OnlyRead, ])
    def ppiSource_detail(request, pk):
        try:
            ppiSource = PPISource.objects.get(pk=pk)
        except PPISource.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = PPISourceSerializer(ppiSource)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = PPISourceSerializer(ppiSource, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            ppiSource.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

