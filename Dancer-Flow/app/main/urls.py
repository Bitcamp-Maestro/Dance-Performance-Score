from django.urls import path
from .views import CommunityView, CommunityVideoView, ShareView, SignView, IndexView, UserView,RankingView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('community/', CommunityView.as_view(), name='community'),
    path('community/view/', CommunityVideoView.as_view(), name='video_view'),
    path('share/', ShareView.as_view(), name='community_share'),
    path('user/', UserView.as_view(), name='user'),
    path('ranking/', RankingView.as_view(), name='ranking'),
]