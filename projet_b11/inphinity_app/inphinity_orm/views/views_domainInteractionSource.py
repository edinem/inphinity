from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

import json
from django.http import HttpResponse

from ..models import DomainInteractionSource
from ..serializers import DomainInteractionSourceSerializer
from ..permissions import *

class DomainInformationSourceView():
    @api_view(['GET', 'POST'])
    @permission_classes([OnlyRead, ])
    def DomainSourceInformation_list(request):
        if request.method == 'GET':
            domSourceInfos = DomainInteractionSource.objects.all()
            serializer = DomainInteractionSourceSerializer(domSourceInfos, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
            serializer = DomainInteractionSourceSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET','PUT','DELETE'])
    @permission_classes([OnlyRead, ])
    def domainInformationSource_detail(request, pk):
        try:
            domInformaSource = DomainInteractionSource.objects.get(pk=pk)
        except DomainInteractionSource.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = DomainInteractionSourceSerializer(domInformaSource)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = DomainInteractionSourceSerializer(domInformaSource, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            domInformaSource.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @api_view(['GET'])
    def ddiPairSourceExists(request, id_ddi, id_source):
        id_ddi_source = {}
        try:
            id_ddi_info_source_queryset = DomainInteractionSource.objects.filter(domain_interaction = id_ddi, information_source = id_source).values_list('id', flat=True)

            id_ddi_info_source = id_ddi_info_source_queryset[0]

            id_ddi_source['id_ddi_iteract_source'] = id_ddi_info_source
            id_ddi_source['exists'] = True

        except Exception as e:
            id_ddi_source['id_ddi_iteract_source'] = -1
            id_ddi_source['exists'] = False

        if request.method == 'GET':
            json_answear = json.dumps(dict(id_ddi_source))
            return HttpResponse(json_answear, content_type='application/json')

