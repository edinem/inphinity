from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from ..models import PPICogScore
from ..serializers import PPICogScoreSerializer
from ..permissions import *

class PPICOGcoreView():
    @api_view(['GET', 'POST'])
    @permission_classes([OnlyRead, ])
    def ppiCogScore_list(request):
        if request.method == 'GET':
            ppiCogsScores = PPICOGcore.objects.all()
            serializer = PPICogScoreSerializer(ppiCogsScores, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
            serializer = PPICogScoreSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET','PUT','DELETE'])
    @permission_classes([OnlyRead, ])
    def ppiCogScore_detail(request, pk):
        try:
            ppiCogsScore = PPICOGcore.objects.get(pk=pk)
        except PPICOGcore.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = PPICogScoreSerializer(ppiCogsScores)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = PPICogScoreSerializer(ppiCogsScores, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            ppiCogsScores.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

