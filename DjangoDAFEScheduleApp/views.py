from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from .models import Article
from rest_framework.response import Response
from rest_framework import status
from .serializer import ArticleSerializer
from django.http import Http404
import json


import sys
sys.path.append("..")
from data_frame import DataFrame
from message import Message

RESOURCE = "1s_u2pPZ3xdu_tBrVy7hriV2xj15OP9evJfVAuzFyZSc"
DF = DataFrame(RESOURCE)
last_req = ''

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class PostReq(APIView):
    global last_req
    def post(self, request, format=None):
        print("POST")
        try:
            print("request.data: ", request.data)
            last_req = request.data
            m = Message(request.data)
        except Exception as e:
            return Response("request body: " + str(request.data)+ "ERROR in PostRequest: " + str(e))#

        return Response(DF.request(m))#


class GetReq(APIView):
    def get(self, format=None):
        print("GET")
        return Response("request body: " + str(last_req))
