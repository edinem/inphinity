from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from ..models import COGInteractionSource
from ..serializers import COGInteractionSourceSerializer
from ..permissions import *

class COGInteractionSourceView():
    @api_view(['GET', 'POST'])
    @permission_classes([OnlyRead, ])
    def cogInteractionSource_list(request):
        if request.method == 'GET':
            cogInteractionsSources = COGInteractionSource.objects.all()
            serializer = COGInteractionSourceSerializer(cogInteractionsSources, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
            serializer = COGInteractionSourceSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET','PUT','DELETE'])
    @permission_classes([OnlyRead, ])
    def cogInteractionSource_detail(request, pk):
        try:
            cogInteractionsSource = COGInteractionSource.objects.get(pk=pk)
        except COGInteractionSource.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = COGInteractionSourceSerializer(cogInteractionsSource)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = COGInteractionSourceSerializer(cogInteractionsSource, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            cogInteractionsSource.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

