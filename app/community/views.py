from django.shortcuts import render

# Create your views here.

def community(request):
  return render(request, "community.html")

def community_view(request):
  return render(request, "community/view.html")

# def index(request):
#   allvideos=Video)