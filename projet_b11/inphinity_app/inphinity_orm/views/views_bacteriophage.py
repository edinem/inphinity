from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
import json
from django.http import HttpResponse

from ..models import Bacteriophage
from ..serializers import BacteriophageSerializer
from ..permissions import *

class BacteriophageViews():
    @api_view(['GET', 'POST'])
    @permission_classes([OnlyRead, ])
    def bacteriophage_list(request):
        if request.method == 'GET':
            bacteriophages = Bacteriophage.objects.all()
            serializer = BacteriophageSerializer(bacteriophages, many=True, context={'request': request})
            return Response(serializer.data)

        elif request.method == 'POST':
            serializer = BacteriophageSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @api_view(['GET','PUT','DELETE'])
    @permission_classes([OnlyRead, ])
    def bacteriophage_detail(request, pk):
        try:
            bacteriophage = Bacteriophage.objects.get(pk=pk)
        except Bacteriophage.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = BacteriophageSerializer(bacteriophage, context={'request': request})
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = BacteriophageSerializer(bacteriophage, data = request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            bacteriophage.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @api_view(['GET'])
    def bacteriumDesignExists(request, designation):

        object_exists = {}
        try:
            bacteriophage = Bacteriophage.objects.get(designation__iexact = designation)
            object_exists['bacteriophage_exists'] = True
            object_exists['id'] = bacteriophage.id
            object_exists['designation'] = bacteriophage.designation
        except Exception as e:
            object_exists['bacteriophage_exists'] = False        
            object_exists['id'] = None
            object_exists['designation'] = None

        if request.method == 'GET':
            json_answear = json.dumps(dict(object_exists))
            return HttpResponse(json_answear, content_type='application/json')

    @api_view(['GET'])
    def bacteriophageByDesignation(request, designation):
        try:
            bacteriophage_obj = Bacteriophage.objects.get(designation__iexact = designation)
            serializer = BacteriophageSerializer(bacteriophage_obj, context={'request': request})
            return Response(serializer.data)

        except Bacteriophage.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
			
    @api_view(['GET'])
    def bacteriophageByAcc(request, accnumber):
        object_exists = {}
        try:
            bacteriophage_obj = Bacteriophage.objects.get(acc_number = accnumber)
            serializer = BacteriophageSerializer(bacteriophage_obj, context={'request': request})
            return Response(serializer.data)

        except Bacteriophage.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)