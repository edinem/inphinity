from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from ..models import Gene
from ..serializers import GeneSerializer
from ..permissions import *

class GeneViews():
    @api_view(['GET', 'POST'])
    @permission_classes([OnlyRead, ])
    def gene_list(request):
        if request.method == 'GET':
            genes = Gene.objects.all()
            serializer = GeneSerializer(genes, many=True, context={'request': request})
            return Response(serializer.data)

        elif request.method == 'POST':
            serializer = GeneSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET','PUT','DELETE'])
    @permission_classes([OnlyRead, ])
    def gene_detail(request, pk):
        try:
            gene = Gene.objects.get(pk=pk)
        except Gene.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = GeneSerializer(gene, context={'request': request})
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = GeneSerializer(gene, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            gene.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)