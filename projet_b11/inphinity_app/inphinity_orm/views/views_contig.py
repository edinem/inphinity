from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from ..models import Contig
from ..serializers import ContigSerializer
from ..permissions import *

class ContigViews():
    @api_view(['GET', 'POST'])
    @permission_classes([OnlyRead, ])
    def contig_list(request):
        if request.method == 'GET':
            contigs = Contig.objects.all()
            serializer = ContigSerializer(contigs, many=True, context={'request': request})
            return Response(serializer.data)

        elif request.method == 'POST':
            serializer = ContigSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET','PUT','DELETE'])
    @permission_classes([OnlyRead, ])
    def contig_detail(request, pk):
        try:
            contig = Contig.objects.get(pk=pk)
        except Contig.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = ContigSerializer(contig, context={'request': request})
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = ContigSerializer(contig, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            contig.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @api_view(['GET'])
    def contigsByOrganism(request, organism_id:int):
        if request.method == 'GET':
            try:
                list_contigs = Contig.objects.filter(organism_id = organism_id)
                serializer = ContigSerializer(list_contigs, many=True, context={'request': request})
                return Response(serializer.data)

            except Exception as e:
                print(e)
                return Response(status=status.HTTP_404_NOT_FOUND)