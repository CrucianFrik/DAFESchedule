from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet, PostReq, GetReq

router = DefaultRouter()
router.register('api', ArticleViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('request/', PostReq.as_view()),
    path('req/', GetReq.as_view())
]
