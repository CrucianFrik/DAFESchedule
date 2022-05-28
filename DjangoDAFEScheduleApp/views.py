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
req = {}

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class PostReq(APIView):
    def post(self, request, format=None):
        global req
        req = request.data
        return Response("request accepted", status=status.HTTP_201_CREATED)


class GetReq(APIView):
    def get(self, request, format=None):
        global req
        m = Message()
        m.add_request(req)

        if not m.check(0):
            return Response({"ERROR"})
        return Response(DF.request(m))