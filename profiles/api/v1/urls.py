from django.urls import path

from profiles.api.v1.views import GetProfileView


urlpatterns = [
    path('<str:username>/', GetProfileView.as_view(), name='get-profile'),
]
