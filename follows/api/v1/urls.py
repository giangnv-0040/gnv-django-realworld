from django.urls import path

from follows.api.v1.views import GetProfileView, FollowUserView


urlpatterns = [
    path('<str:username>/', GetProfileView.as_view(), name='get-profile'),
    path('<str:username>/follow/', FollowUserView.as_view(), name='follow-user'),
]
