from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from ..models import COG
from ..serializers import COGSerializer
from ..permissions import *

class COGView():
    @api_view(['GET', 'POST'])
    @permission_classes([OnlyRead, ])
    def cog_list(request):
        if request.method == 'GET':
            cogs = COG.objects.all()
            serializer = COGSerializer(cogs, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
            serializer = COGSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET','PUT','DELETE'])
    @permission_classes([OnlyRead, ])
    def cog_detail(request, pk):
        try:
            cog = COG.objects.get(pk=pk)
        except COG.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = COGSerializer(cog)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = COGSerializer(cog, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            cog.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

