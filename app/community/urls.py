from django.urls import path 
from . import views

urlpatterns=[
  path("community/", views.community, name="community"),
  path("community/view/", views.community_view, name="community_view")
]