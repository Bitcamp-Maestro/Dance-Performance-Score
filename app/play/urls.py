from django.urls import path, include
from django.urls.resolvers import URLPattern
from .views import PlayView, OptionView



urlpatterns = [
    path('', PlayView.as_view()),
    path('option/', OptionView.as_view()),
    path('api/options', OptionView.as_view()),
]  