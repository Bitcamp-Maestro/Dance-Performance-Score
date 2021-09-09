from django.urls import path, include
from django.urls.resolvers import URLPattern
from .views import CommunityView, CommunityVideoView, ShareView, SignView, IndexView, UserView



urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('sign/', SignView.as_view()),
    path('community/', CommunityView.as_view()),
    path('community/view/', CommunityVideoView.as_view()),
    path('share/', ShareView.as_view()),
    path('user/', UserView.as_view()),
]