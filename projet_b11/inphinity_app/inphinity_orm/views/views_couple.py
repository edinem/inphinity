from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from ..models import Couple
from ..serializers import CoupleSerializer
from ..permissions import *

class CoupleView():
    @api_view(['GET', 'POST'])
    @permission_classes([OnlyRead, ])
    def couple_list(request):
        if request.method == 'GET':
            couples = Couple.objects.all()
            serializer = CoupleSerializer(couples, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
            serializer = CoupleSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET','PUT','DELETE'])
    @permission_classes([OnlyRead, ])
    def couple_detail(request, pk):
        try:
            couple = Couple.objects.get(pk=pk)
        except Couple.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = CoupleSerializer(couple)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = CoupleSerializer(couple, data = request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            couple.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @api_view(['GET'])
    def coupleDetailByIdBactIdPhage(request, idBact, idPhage):
        try:
            couple = Couple.objects.get(bacterium = idBact, bacteriophage =idPhage)
        except Couple.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = CoupleSerializer(couple)
            return Response(serializer.data)
