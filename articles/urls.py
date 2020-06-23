from django.urls import path
from articles import views

urlpatterns = [
    path('', views.api_root),
    path('article/', views.ArticleListGeneric.as_view(), name='article-list'),
    path('article/<int:pk>', views.ArticleDetailGeneric.as_view(), name='article-detail'),
    path('user/', views.UserList.as_view(), name='user-list'),
]