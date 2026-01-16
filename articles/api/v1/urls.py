from django.urls import path

from articles.api.v1.views import ArticlesView, ArticleDetailView, FavoriteArticleView


urlpatterns = [
    path('articles/', ArticlesView.as_view(), name='articles'),
    path('articles/<str:slug>/', ArticleDetailView.as_view(), name='article-detail'),
    path('articles/<str:slug>/favorite/', FavoriteArticleView.as_view(), name='favorite-article'),
]
