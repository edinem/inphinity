from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from ..models import SourceData
from ..serializers import SourceDataSerializer
from ..permissions import *

class SourceDataView():
    @api_view(['GET', 'POST'])
    @permission_classes([OnlyRead, ])
    def sourceData_list(request):
        print(request.user)
        print(type(request))
        if request.method == 'GET':
            sourceDatas = SourceData.objects.all()
            serializer = SourceDataSerializer(sourceDatas, many=True, context={'request': request})
            return Response(serializer.data)

        elif request.method == 'POST':
            serializer = SourceDataSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @api_view(['GET','PUT','DELETE'])
    @permission_classes([OnlyRead, ])
    def sourceData_detail(request, pk):
        try:
            sourceData = SourceData.objects.get(pk=pk)
        except sourceData.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = SourceDataSerializer(sourceData, context={'request': request})
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = SourceDataSerializer(sourceData, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            sourceData.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)