from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
import json
from django.http import HttpResponse

from ..models import Strain
from ..serializers import StrainSerializer
from ..permissions import *

class StrainViews():
    @api_view(['GET', 'POST'])
    @permission_classes([OnlyRead, ])
    def strain_list(request):
        if request.method == 'GET':
            strains = Strain.objects.all()
            serializer = StrainSerializer(strains, many=True, context={'request': request})
            return Response(serializer.data)

        elif request.method == 'POST':
            serializer = StrainSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET','PUT','DELETE'])
    @permission_classes([OnlyRead, ])
    def strain_detail(request, pk):
        try:
            strain = Strain.objects.get(pk=pk)
        except Strain.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = StrainSerializer(strain, context={'request': request})
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = StrainSerializer(strain, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            strain.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @api_view(['GET'])
    def strainDesignSpecieExistes(request, designation, fk_specie):

        object_exists = {}
        try:
            strain = Strain.objects.get(designation__iexact = designation, specie_id = fk_specie)
            object_exists['strain_exists'] = True
            object_exists['id'] = strain.id
            object_exists['designation'] = strain.designation
            object_exists['specie'] = strain.specie_id
        except Exception as e:
            object_exists['strain_exists'] = False            
            object_exists['id'] = None
            object_exists['designation'] = None
            object_exists['specie'] = None

        if request.method == 'GET':
            json_answear = json.dumps(dict(object_exists))
            return HttpResponse(json_answear, content_type='application/json')