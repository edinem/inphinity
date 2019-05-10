from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from ..models import COGSourceInformation
from ..serializers import COGSourceInformationSerializer
from ..permissions import *


class COGSourceInformationView():
    @api_view(['GET', 'POST'])
    @permission_classes([OnlyRead, ])
    def cogSourceInformation_list(request):
        if request.method == 'GET':
            cogInformations = COGSourceInformation.objects.all()
            serializer = COGSourceInformationSerializer(cogInformations, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
            serializer = COGSourceInformationSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET','PUT','DELETE'])
    @permission_classes([OnlyRead, ])
    def cogSourceInformation_detail(request, pk):
        try:
            cogInformation = COGSourceInformation.objects.get(pk=pk)
        except COGSourceInformation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = COGSourceInformationSerializer(cogInformation)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = COGSourceInformationSerializer(cogInformation, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            cogInformation.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

