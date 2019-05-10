from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from ..models import PFAMMethodScore
from ..serializers import PFAMMethodScoreSerializer
from ..permissions import *

class PFAMMethodScoreView():
    @api_view(['GET', 'POST'])
    @permission_classes([OnlyRead, ])
    def pfamMethodScore_list(request):
        if request.method == 'GET':
            pfamMethodScores = PFAMMethodScore.objects.all()
            serializer = PFAMMethodScoreSerializer(pfamMethodScores, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
            serializer = PFAMMethodScoreSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET','PUT','DELETE'])
    @permission_classes([OnlyRead, ])
    def pfamMethodScore_detail(request, pk):
        try:
            pfamMethodScore = PFAMMethodScore.objects.get(pk=pk)
        except PFAMMethodScore.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = PFAMMethodScoreSerializer(pfamMethodScore)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = PFAMMethodScoreSerializer(pfamMethodScore, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            pfamMethodScore.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

