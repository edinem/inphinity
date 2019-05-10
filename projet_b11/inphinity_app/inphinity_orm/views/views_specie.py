from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from ..models import Specie
from ..serializers import SpecieSerializer
from ..permissions import *

class SpecieViews():
    @api_view(['GET', 'POST'])
    @permission_classes([OnlyRead, ])
    def specie_list(request):
        if request.method == 'GET':
            species = Specie.objects.all()
            serializer = SpecieSerializer(species, many=True, context={'request': request})
            return Response(serializer.data)

        elif request.method == 'POST':
            serializer = SpecieSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET','PUT','DELETE'])
    @permission_classes([OnlyRead, ])
    def specie_detail(request, pk):
        try:
            specie = Specie.objects.get(pk=pk)
        except Specie.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = SpecieSerializer(specie, context={'request': request})
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = SpecieSerializer(specie, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            specie.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)