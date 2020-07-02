from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics
from rest_framework import permissions
from rest_framework.reverse import reverse
from rest_framework.pagination import PageNumberPagination

from django.contrib.auth.models import User
from django.core.paginator import Paginator

from django.http import Http404
from articles.models import Article
from articles.serializers import ArticleSerializer, UserSerializer
from articles.permissions import IsOwnerOrReadOnly

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'articles': reverse('article-list', request=request, format=format)
    })


class CustomPaginator(PageNumberPagination):
    page_size = 10

    def generate_response(self, queryset, serializer, request):
        page_data = self.paginate_queryset(queryset, request)
        serialized_page = serializer(page_data, many=True)
        return self.get_paginated_response(serialized_page.data)

class ArticleListByUser(APIView):
    def get(self, request, pk, num=1, format=None):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(status=404)
        p = CustomPaginator()
        return p.generate_response(Article.objects.filter(owner=pk), ArticleSerializer, request)
        



@api_view(['GET'])
def article_list_by_user(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=404)
    
    serializer = ArticleSerializer(Article.objects.filter(owner=pk), many=True)
    return Response(serializer.data)

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer





class ArticleListGeneric(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ArticleDetailGeneric(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class ArticleListMixin(mixins.ListModelMixin, 
                        mixins.CreateModelMixin, 
                        generics.GenericAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class ArticleDetailMixin(mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        generics.GenericAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ArticleList(APIView):

    def get(self, request, format=None):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ArticleDetail(APIView):

    def get_object(self, pk):
        try:
            return Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        article = self.get_object(pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        article = self.get_object(pk)
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk, format=None):
        article = self.get_object(pk)
        article.delete()
        return Response(status=204)        
        
@api_view(['GET', 'POST'])
def article_list (request):
    """
    List all articles, or create a new article.
    """

    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
def article_detail(request, pk):
    try:
        article = Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        article.delete()
        return Response(status=204)        