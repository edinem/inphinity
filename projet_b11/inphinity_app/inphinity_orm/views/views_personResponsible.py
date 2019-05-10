from rest_framework import status
from rest_framework.decorators import api_view, permission_classes


from rest_framework.response import Response

from ..permissions import *

from rest_framework.decorators import api_view
from ..models import PersonResponsible
from ..serializers import PersonResponsibleSerializer

class PersonResponsibleView():

    @api_view(['GET', 'POST'])
    @permission_classes([OnlyRead, ])
    def personeResponsible_list(request):

        if request.method == 'GET':
            personresponsibles = PersonResponsible.objects.all()
            serializer = PersonResponsibleSerializer(personresponsibles, many=True, context={'request': request})


            return Response(serializer.data)

        elif request.method == 'POST':
            serializer = PersonResponsibleSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET','PUT','DELETE'])
    @permission_classes([OnlyRead, ])
    def personeResponsible_detail(request, pk):
        try:
            personResponsible = PersonResponsible.objects.get(pk=pk)
        except personResponsible.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = PersonResponsibleSerializer(personResponsible, context={'request': request})
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = PersonResponsibleSerializer(personResponsible, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            personResponsible.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
