from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from ..models import Family
from ..serializers import FamilySerializer
from ..permissions import *

class FamilyView():
    @api_view(['GET', 'POST'])
    @permission_classes([OnlyRead, ])
    def family_list(request):
        if request.method == 'GET':
            families = Family.objects.all()
            serializer = FamilySerializer(families, many=True, context={'request': request})
            #serializer = FamilySerializer(families, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
            serializer = FamilySerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET','PUT','DELETE'])
    @permission_classes([OnlyRead, ])
    def family_detail(request, pk):
        try:
            family = Family.objects.get(pk=pk)
        except Family.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = FamilySerializer(family, context={'request': request})
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = FamilySerializer(family, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            family.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

