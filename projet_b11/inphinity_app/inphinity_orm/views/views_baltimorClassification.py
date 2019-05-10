from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from ..models import BaltimoreClassification
from ..serializers import BaltimorClassificationSerializer
from ..permissions import *

class BaltimoreClassificationView():
    @api_view(['GET', 'POST'])
    @permission_classes([OnlyRead, ])
    def baltimoreClassification_list(request):
        if request.method == 'GET':
            baltimoreClassifications = BaltimoreClassification.objects.all()
            serializer = BaltimorClassificationSerializer(baltimoreClassifications, many=True, context={'request': request})
            return Response(serializer.data)

        elif request.method == 'POST':
            serializer = BaltimorClassificationSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET','PUT','DELETE'])
    @permission_classes([OnlyRead, ])
    def baltimoreClassification_detail(request, pk):
        try:
            baltimoreClassification = BaltimoreClassification.objects.get(pk=pk)
        except baltimoreClassification.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = BaltimorClassificationSerializer(baltimoreClassification, context={'request': request})
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = BaltimorClassificationSerializer(baltimoreClassification, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            baltimoreClassification.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)