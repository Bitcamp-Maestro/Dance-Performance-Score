from django.urls import path, include
from django.urls.resolvers import URLPattern
from .views import ErrorView, CommunityView, CommunityVideoView, ShareView, IndexView, TestView, RankingView
from . import views


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('test', TestView.as_view(), name='index'),
    path('error/', ErrorView.as_view(), name='error'),
    path('community/', CommunityView.as_view(), name='community'),
    path('community/view/<str:play_id>/', CommunityVideoView.as_view(), name='video_view'),
    path('share/', ShareView.as_view(), name='community_share'),
    path('ranking/', RankingView.as_view(), name='ranking'),
    
]