from distutils.command.install_egg_info import safe_name
from email.mime import application
import imp
import json
from math import ceil
from multiprocessing import managers
from os import stat
from tkinter.messagebox import RETRY
from turtle import st
from urllib import response
from .models import Application
from .models import Favourite
from .models import Reject
from rest_framework import status
from django.db.models import Count, Q
from .serializers import ApplicationSerializer
from .serializers import FavouriteSerializer
from .serializers import RejectSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def postApplication(request):
    if request.method == 'POST':
        serializer = ApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def postFavourite(request):
    if request.method == 'POST':
        serializer = FavouriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def postReject(request):
    if request.method == 'POST':
        serializer = RejectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
