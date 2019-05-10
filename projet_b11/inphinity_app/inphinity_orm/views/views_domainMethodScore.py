from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from ..models import DomainMethodScore
from ..serializers import DomainMethodScoreSerializer
from ..permissions import *

class DomainMethodScoreView():
    @api_view(['GET', 'POST'])
    @permission_classes([OnlyRead, ])
    def domainMethodScore_list(request):
        if request.method == 'GET':
            domainMethScores = DomainMethodScore.objects.all()
            serializer = DomainMethodScoreSerializer(domainMethScores, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
            serializer = DomainMethodScoreSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET','PUT','DELETE'])
    @permission_classes([OnlyRead, ])
    def domainMethodScore_detail(request, pk):
        try:
            domainMethScore = DomainMethodScore.objects.get(pk=pk)
        except DomainMethodScore.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = DomainMethodScoreSerializer(domainMethScore)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = DomainMethodScoreSerializer(domainMethScore, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            domainMethScore.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

