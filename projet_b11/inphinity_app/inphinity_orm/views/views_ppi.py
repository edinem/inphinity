from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from ..models import PPI
from ..serializers import PPISerializer
from ..permissions import *

class PPIView():
    @api_view(['GET', 'POST'])
    @permission_classes([OnlyRead, ])
    def ppi_list(request):
        if request.method == 'GET':
            ppis = PPI.objects.all()
            serializer = PPISerializer(ppis, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
            serializer = PPISerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET','PUT','DELETE'])
    @permission_classes([OnlyRead, ])
    def ppi_detail(request, pk):
        try:
            ppi = PPI.objects.get(pk=pk)
        except PPI.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = PPISerializer(ppi)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = PPISerializer(ppi, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            ppi.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

