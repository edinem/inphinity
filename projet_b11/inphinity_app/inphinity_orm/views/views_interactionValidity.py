from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from ..models import InteractionValidity
from ..serializers import InteractionValiditySerializer
from ..permissions import *

class InteractionValidityView():
    @api_view(['GET', 'POST'])
    @permission_classes([OnlyRead, ])
    def interactionValidity_list(request):
        if request.method == 'GET':
            intValidities = InteractionValidity.objects.all()
            serializer = InteractionValiditySerializer(intValidities, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
            serializer = InteractionValiditySerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET','PUT','DELETE'])
    @permission_classes([OnlyRead, ])
    def interactionValidity_detail(request, pk):
        try:
            intValidity = InteractionValidity.objects.get(pk=pk)
        except InteractionValidity.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = InteractionValiditySerializer(intValidity)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = InteractionValiditySerializer(intValidity, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            intValidity.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

