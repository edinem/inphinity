from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
import json
from django.http import HttpResponse

from ..models import DomainInterationsPair
from ..models import Domain
from ..serializers import DomainInteractionPairSerializer
from ..permissions import *

class DomainInterationsPairView():
    @api_view(['GET', 'POST'])
    @permission_classes([OnlyRead, ])
    def domainInteractionPair_list(request):
        if request.method == 'GET':
            domInterPairs = DomainInterationsPair.objects.all()
            serializer = DomainInteractionPairSerializer(domInterPairs, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
            serializer = DomainInteractionPairSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET','PUT','DELETE'])
    @permission_classes([OnlyRead, ])
    def domainInteractionPair_detail(request, pk):
        try:
            domInterPair = DomainInterationsPair.objects.get(pk=pk)
        except DomainInterationsPair.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = DomainInteractionPairSerializer(domInterPair)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = DomainInteractionPairSerializer(domInterPair, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            domInterPair.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @api_view(['GET'])
    @permission_classes([OnlyRead, ])
    def ddiPairExists(request, pfam_a, pfam_b):
        pfam_a = pfam_a.upper()
        pfam_b = pfam_b.upper()

        id_ddi_interaction = {}
        try:
            pfam_a_id_queryset = Domain.objects.filter(designation = pfam_a).values_list('id', flat=True)
            pfam_b_id_queryset = Domain.objects.filter(designation = pfam_b).values_list('id', flat=True)

            pfam_a_id = pfam_a_id_queryset[0]
            pfam_b_id = pfam_b_id_queryset[0]

            # test dom_a = dom_a and dom_b = dom_b
            existance_ddi = DomainInterationsPair.objects.filter(domain_a = pfam_a_id, domain_b = pfam_b_id).exists()

            if existance_ddi == False:
                id_ddi_interaction_queryset = DomainInterationsPair.objects.filter(domain_a_id = pfam_b_id, domain_b_id = pfam_a_id).values_list('id', flat=True)
            else:
                id_ddi_interaction_queryset = DomainInterationsPair.objects.filter(domain_a_id = pfam_a_id, domain_b_id = pfam_b_id).values_list('id', flat=True)

            id_ddi_interaction['exists'] = True
            id_ddi_interaction['id_ddi_interaction'] = id_ddi_interaction_queryset[0]
        except Exception as e:
            id_ddi_interaction['id_ddi_interaction'] = -1
            id_ddi_interaction['exists'] = False

        if request.method == 'GET':
            json_answear = json.dumps(dict(id_ddi_interaction))
            return HttpResponse(json_answear, content_type='application/json')
