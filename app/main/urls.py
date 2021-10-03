from django.urls import path, include
from django.urls.resolvers import URLPattern
from .views import CommunityView, CommunityVideoView, ShareView, SignView, IndexView, UserView
from . import views


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('sign/', SignView.as_view(), name='sign'),
    path('community/', CommunityView.as_view(), name='community'),
    path('community/view/', CommunityVideoView.as_view(), name='video_view'),
    path('share/', ShareView.as_view(), name='community_share'),
    path('user/', UserView.as_view(), name='user'),
    
    
    path('register/', views.register),
    path('login/', views.login),
    path('logout/', views.logout),
    path('home/', views.home),
]