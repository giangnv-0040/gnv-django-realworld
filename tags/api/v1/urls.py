from django.urls import path

from tags.api.v1.views import TagsView


urlpatterns = [
    path('tags/', TagsView.as_view(), name='tags'),
]
