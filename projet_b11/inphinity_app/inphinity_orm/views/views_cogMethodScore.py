from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from ..models import COGMethodScore
from ..serializers import COGMethodScoreSerializer
from ..permissions import *

class COGMethodScoreView():
    @api_view(['GET', 'POST'])
    @permission_classes([OnlyRead, ])

    def cogMethodScore_list(request):
        if request.method == 'GET':
            cogmethodScores = COGMethodScore.objects.all()
            serializer = COGMethodScoreSerializer(cogmethodScores, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
            serializer = COGMethodScoreSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET','PUT','DELETE'])
    @permission_classes([OnlyRead, ])
    def cogMethodScore_detail(request, pk):
        try:
            cogmethodScore = COGMethodScore.objects.get(pk=pk)
        except COGMethodScore.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = COGMethodScoreSerializer(cogmethodScore)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = COGMethodScoreSerializer(cogmethodScore, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            cogmethodScore.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

