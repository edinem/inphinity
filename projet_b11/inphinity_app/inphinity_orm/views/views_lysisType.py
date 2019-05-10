from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from ..models import LysisType
from ..serializers import LysisTypeSerializer
from ..permissions import *

class LysisTypeView():
    @api_view(['GET', 'POST'])
    @permission_classes([OnlyRead, ])
    def lysisType_list(request):
        if request.method == 'GET':
            lysistypes = LysisType.objects.all()
            serializer = LysisTypeSerializer(lysistypes, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
            serializer = LysisTypeSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET','PUT','DELETE'])
    @permission_classes([OnlyRead, ])
    def lysisType_detail(request, pk):
        try:
            lysisType = LysisType.objects.get(pk=pk)
        except LysisType.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = LysisTypeSerializer(lysisType)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = LysisTypeSerializer(lysisType, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            lysisType.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

