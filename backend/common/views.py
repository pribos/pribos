from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

# Create your views here.


@api_view(['GET'])
def getFront(request):
    #검색어
    return Response("HI")



