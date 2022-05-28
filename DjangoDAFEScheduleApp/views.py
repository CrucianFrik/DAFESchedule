from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from .models import Article
from rest_framework.response import Response
from rest_framework import status
from .serializer import ArticleSerializer
from django.http import Http404

import sys
sys.path.append("..")
from data_frame import DataFrame
from message import Message

DF = DataFrame("1s_u2pPZ3xdu_tBrVy7hriV2xj15OP9evJfVAuzFyZSc")
#req = {}

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class PostReq(APIView):
    def post(self, request, format=None):
        print("POST")
        return Response(req, status=status.HTTP_201_CREATED)


class GetReq(APIView):
    def get(self, request, format=None):
        print("GET")
        try:
            m = Message(request.data)
        except Exception as e:
            return Response("ERROR in GetReq " + str(e))

        return Response(DF.request(m))