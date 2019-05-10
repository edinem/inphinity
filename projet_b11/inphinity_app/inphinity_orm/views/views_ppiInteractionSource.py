from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from ..models import PPIInteractionSource
from ..serializers import PPIInteractionSourceSerializer
from ..permissions import *

class PPIInteractionSourceView():
    @api_view(['GET', 'POST'])
    @permission_classes([OnlyRead, ])
    def ppiInteractionSource_list(request):
        if request.method == 'GET':
            ppiInteracSources = PPIInteractionSource.objects.all()
            serializer = PPIInteractionSourceSerializer(ppiInteracSources, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
            serializer = PPIInteractionSourceSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET','PUT','DELETE'])
    @permission_classes([OnlyRead, ])
    def ppiInteractionSource_detail(request, pk):
        try:
            ppiInteracSource = PPIInteractionSource.objects.get(pk=pk)
        except PPIInteractionSource.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = PPIInteractionSourceSerializer(ppiInteracSource)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = PPIInteractionSourceSerializer(ppi, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            ppiInteracSource.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

