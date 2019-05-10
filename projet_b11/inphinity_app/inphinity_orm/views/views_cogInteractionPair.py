from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from ..models import COGInterationPair
from ..serializers import COGInterationPairSerializer
from ..permissions import *


class COGInterationPairView():
    @api_view(['GET', 'POST'])
    @permission_classes([OnlyRead, ])
    def cogInteractionPair_list(request):
        if request.method == 'GET':
            cogInteractions = COGInterationPair.objects.all()
            serializer = COGInterationPairSerializer(cogInteractions, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
            serializer = COGInterationPairSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET','PUT','DELETE'])
    @permission_classes([OnlyRead, ])
    def cogInteractionPair_detail(request, pk):
        try:
            cogInteraction = COGInterationPair.objects.get(pk=pk)
        except COGInterationPair.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = COGInterationPairSerializer(cogInteraction)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = COGInterationPairSerializer(cogInteraction, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            cogInteraction.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

