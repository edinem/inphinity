from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from ..models import ProteinCog
from ..serializers import ProteinCogSerializer
from ..permissions import *

class ProteinCogView():
    @api_view(['GET', 'POST'])
    @permission_classes([OnlyRead, ])
    def proteinCog_list(request):
        if request.method == 'GET':
            proteinCogs = ProteinCog.objects.all()
            serializer = ProteinCogSerializer(proteinCogs, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
            serializer = ProteinCogSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET','PUT','DELETE'])
    @permission_classes([OnlyRead, ])
    def proteinCog_detail(request, pk):
        try:
            proteinCog = ProteinCog.objects.get(pk=pk)
        except ProteinCog.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = ProteinCogSerializer(proteinCog)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = ProteinCogSerializer(proteinCog, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            proteinCog.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

