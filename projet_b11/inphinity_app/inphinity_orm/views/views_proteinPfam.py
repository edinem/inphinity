from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from ..models import ProteinPfam
from ..serializers import ProteinPFAMSerializer
from ..permissions import *

class ProteinPFAMViews():
    @api_view(['GET', 'POST'])
    @permission_classes([OnlyRead, ])
    def proteinPfam_list(request):
        if request.method == 'GET':
            proteinsPfam = ProteinPfam.objects.all()
            serializer = ProteinPFAMSerializer(proteinsPfam, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
            serializer = ProteinPFAMSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET','PUT','DELETE'])
    @permission_classes([OnlyRead, ])
    def proteinPfam_detail(request, pk):
        try:
            proteinPfam = ProteinPfam.objects.get(pk=pk)
        except ProteinPfam.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = ProteinPFAMSerializer(proteinPfam)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = ProteinPFAMSerializer(proteinPfam, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            proteinPfam.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)