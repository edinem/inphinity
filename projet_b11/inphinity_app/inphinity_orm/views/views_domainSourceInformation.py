from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from ..models import DomainSourceInformation
from ..serializers import DomainSourceInformationSerializer
from ..permissions import *

class DomainSourceInformationView():
    @api_view(['GET', 'POST'])
    @permission_classes([OnlyRead, ])
    def DomainSourceInformation_list(request):
        if request.method == 'GET':
            domSourceInfs = DomainSourceInformation.objects.all()
            serializer = DomainSourceInformationSerializer(domSourceInfs, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
            serializer = DomainSourceInformationSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET','PUT','DELETE'])
    @permission_classes([OnlyRead, ])
    def domainSourceInteractionPair_detail(request, pk):
        try:
            domSourceInf = DomainSourceInformation.objects.get(pk=pk)
        except DomainSourceInformation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = DomainSourceInformationSerializer(domSourceInf)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = DomainSourceInformationSerializer(domSourceInf, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            domSourceInf.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

