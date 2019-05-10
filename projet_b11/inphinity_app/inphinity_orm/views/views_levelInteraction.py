from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from ..models import LevelInteraction
from ..serializers import LevelInteractionSerializer
from ..permissions import *

class LevelInteractionView():
    @api_view(['GET', 'POST'])
    @permission_classes([OnlyRead, ])
    def levelInteraction_list(request):
        if request.method == 'GET':
            levelInteractions = LevelInteraction.objects.all()
            serializer = LevelInteractionSerializer(levelInteractions, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
            serializer = LevelInteractionSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET','PUT','DELETE'])
    @permission_classes([OnlyRead, ])
    def interactionValidity_detail(request, pk):
        try:
            levelInteraction = LevelInteraction.objects.get(pk=pk)
        except LevelInteraction.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = LevelInteractionSerializer(levelInteraction)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = LevelInteractionSerializer(levelInteraction, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            levelInteraction.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

