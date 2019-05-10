from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from ..models import PPIPFAMScore
from ..serializers import PPIPFAMScoreSerializer
from ..permissions import *

class PPIPFAMScoreView():
    @api_view(['GET', 'POST'])
    @permission_classes([OnlyRead, ])
    def ppiPfamScore_list(request):
        if request.method == 'GET':
            ppiPfamScores = PPIPFAMScore.objects.all()
            serializer = PPIPFAMScoreSerializer(ppiPfamScores, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
            serializer = PPIPFAMScoreSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET','PUT','DELETE'])
    @permission_classes([OnlyRead, ])
    def ppiPfamScore_detail(request, pk):
        try:
            ppiPfamScore = PPIPFAMScore.objects.get(pk=pk)
        except PPIPFAMScore.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = PPIPFAMScoreSerializer(ppiPfamScore)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = PPIPFAMScoreSerializer(ppiPfamScore, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            ppiPfamScore.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

