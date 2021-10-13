from django.db.models import query
from django.shortcuts import render
import rest_framework
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ProductSerializer
from .models import Product

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from product.serializers import UserSerializer, GroupSerializer


# Create your views here.

class ProductListAPI(APIView):
    def get(self, req):
        queryset = Product.objects.all()
        print(queryset)
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    """
    사용자를 보거나 편집할 수 있는 API endpoint
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    사용자를 보거나 편집할 수 있는 API endpoint
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
