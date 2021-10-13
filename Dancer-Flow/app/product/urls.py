from django.urls import path, include
from django.urls.resolvers import URLPattern
from .views import ProductListAPI

URLPattern = [
    path('', ProductListAPI.as_view()),
]