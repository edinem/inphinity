from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from ..models import DomainInteractionScore
from ..serializers import DomainInteractionScoreSerializer
from ..permissions import *

class DomainInteractionScoreView():
    @api_view(['GET', 'POST'])
    @permission_classes([OnlyRead, ])
    def domainInteractionScore_list(request):
        if request.method == 'GET':
            domainInteractScores = DomainInteractionScore.objects.all()
            serializer = DomainInteractionScoreSerializer(domainInteractScores, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
            serializer = DomainInteractionScoreSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET','PUT','DELETE'])
    @permission_classes([OnlyRead, ])
    def domainInteractionScore_detail(request, pk):
        try:
            domainInteractScore = DomainInteractionScore.objects.get(pk=pk)
        except DomainInteractionScore.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = DomainInteractionScoreSerializer(domainInteractScore)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = DomainInteractionScoreSerializer(domainInteractScore, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            domainInteractScore.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

