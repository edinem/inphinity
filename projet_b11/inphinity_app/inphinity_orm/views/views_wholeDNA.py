from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from ..models import WholeDNA
from ..serializers import WholeDNASerializer
from ..permissions import *

class WholeDNAViews():
    @api_view(['GET', 'POST'])
    @permission_classes([OnlyRead, ])
    def wholeDNA_list(request):
        if request.method == 'GET':
            wholeDNAs = WholeDNA.objects.all()
            serializer = WholeDNASerializer(wholeDNAs, many=True, context={'request': request})
            return Response(serializer.data)

        elif request.method == 'POST':
            serializer = WholeDNASerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET','PUT','DELETE'])
    @permission_classes([OnlyRead, ])
    def wholeDNA_detail(request, pk):
        try:
            wholeDNA = WholeDNA.objects.get(pk=pk)
        except WholeDNA.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = WholeDNASerializer(wholeDNA, context={'request': request})
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = WholeDNASerializer(wholeDNA, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            wholeDNA.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @api_view(['GET'])
    @permission_classes([OnlyRead, ])
    def wholeDNAByOrganism(request, organism_id:int):
        if request.method == 'GET':
            try:
                whole_dna_obj = WholeDNA.objects.get(organism_id = organism_id)
                serializer = WholeDNASerializer(whole_dna_obj , context={'request': request})
                return Response(serializer.data)

            except Exception as e:
                print(e)
                return Response(status=status.HTTP_404_NOT_FOUND)
