from django.urls import path

from comments.api.v1.views import CommentsView, CommentDetailView

urlpatterns = [
    path('articles/<slug:slug>/comments/', CommentsView.as_view(), name='article-comments'),
    path('articles/<slug:slug>/comments/<int:id>/', CommentDetailView.as_view(), name='comment-detail'),
]
