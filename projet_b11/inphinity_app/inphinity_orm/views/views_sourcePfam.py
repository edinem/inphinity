from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from ..models import SourcePFAM
from ..serializers import SourcePFAMSerializer
from ..permissions import *

class SourcePFAMView():
    @api_view(['GET', 'POST'])
    @permission_classes([OnlyRead, ])
    def sourcePfam_list(request):
        if request.method == 'GET':
            sourcePFAMs = SourcePFAM.objects.all()
            serializer = SourcePFAMSerializer(sourcePFAMs, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
            serializer = SourcePFAMSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET','PUT','DELETE'])
    @permission_classes([OnlyRead, ])
    def sourcePfam_detail(request, pk):
        try:
            sourcePFAM = SourcePFAM.objects.get(pk=pk)
        except sourcePFAM.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = SourcePFAMSerializer(sourcePFAM)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = SourcePFAMSerializer(sourcePFAM, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            sourcePFAM.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

