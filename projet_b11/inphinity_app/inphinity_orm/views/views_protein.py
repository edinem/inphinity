from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from ..models import Protein
from ..serializers import ProteinSerializer
from ..permissions import *

class ProteinViews():
    @api_view(['GET', 'POST'])
    @permission_classes([OnlyRead, ])
    def protein_list(request):
        if request.method == 'GET':
            proteins = Protein.objects.all()
            serializer = ProteinSerializer(proteins, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
            serializer = ProteinSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET','PUT','DELETE'])
    @permission_classes([OnlyRead, ])
    def protein_detail(request, pk):
        try:
            protein = Protein.objects.get(pk=pk)
        except Protein.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = ProteinSerializer(protein)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = ProteinSerializer(protein, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            protein.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @api_view(['GET'])
    def protein_by_organism(request, organism_id):        

        if request.method == 'GET':
            try:
                proteins = Protein.objects.filter(organism_id = organism_id)
                serializer = ProteinSerializer(proteins , many=True)
                return Response(serializer.data)
            except Exception as e:
                return Response(status=status.HTTP_404_NOT_FOUND)
