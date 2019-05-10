from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from ..models import SourceCog
from ..serializers import SourceCogSerializer
from ..permissions import *

class SourceCogView():
    @api_view(['GET', 'POST'])
    @permission_classes([OnlyRead, ])
    def sourceCog_list(request):
        if request.method == 'GET':
            sourceCogs = SourceCog.objects.all()
            serializer = SourceCogSerializer(sourceCogs, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
            serializer = SourceCogSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET','PUT','DELETE'])
    @permission_classes([OnlyRead, ])
    def sourceCog_detail(request, pk):
        try:
            sourceCog = SourceCog.objects.get(pk=pk)
        except SourceCog.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = SourceCogSerializer(sourceCog)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = SourceCogSerializer(sourceCog, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            sourceCog.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

