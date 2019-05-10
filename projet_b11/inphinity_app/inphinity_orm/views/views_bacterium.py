from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
import json
from django.http import HttpResponse

from ..models import Bacterium
from ..models import Organism
from ..serializers import BacteriumSerializer
from ..permissions import *

class BacteriumViews():
    @api_view(['GET', 'POST'])
    @permission_classes([OnlyRead, ])
    def bacterium_list(request):
        print("sdsdsd")
        if request.method == 'GET':
            bacteria = Bacterium.objects.all()
            serializer = BacteriumSerializer(bacteria, many=True, context={'request': request})
            return Response(serializer.data)

        elif request.method == 'POST':
            serializer = BacteriumSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET','PUT','DELETE'])
    @permission_classes([OnlyRead, ])
    def bacterium_detail(request, pk):
        try:
            bacterium = Bacterium.objects.get(pk=pk)
        except Bacterium.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = BacteriumSerializer(bacterium, context={'request': request})
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = BacteriumSerializer(bacterium, data = request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            bacterium.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @api_view(['GET'])
    def bacteriumAccExists(request, accnumber):

        object_exists = {}
        try:
            object_exists['bacterium_exists'] = Bacterium.objects.filter(acc_number = accnumber).exists()
            print(object_exists)
        except Exception as e:
            object_exists['bacterium_exists'] = False

        if request.method == 'GET':
            object_exists['accnumber'] = accnumber
            json_answear = json.dumps(dict(value=object_exists))
            return HttpResponse(json_answear, content_type='application/json')

    @api_view(['GET'])
    def bacteriumByAcc(request, accnumber):
        object_exists = {}
        try:
            bacterium_obj = Bacterium.objects.get(acc_number = accnumber)
            serializer = BacteriumSerializer(bacterium_obj, context={'request': request})
            return Response(serializer.data)

        except Bacterium.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
            