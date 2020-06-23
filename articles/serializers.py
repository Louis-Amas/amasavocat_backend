from django.contrib.auth.models import User
from rest_framework import serializers

from articles.models import Article

class UserSerializer(serializers.HyperlinkedModelSerializer):
    #articles = serializers.PrimaryKeyRelatedField(many=True, queryset=Article.objects.all())
    articles = serializers.HyperlinkedRelatedField(many=True, view_name='article-detail', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'articles']

class ArticleSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Article
        fields = ['id', 'title', 'body', 'owner']