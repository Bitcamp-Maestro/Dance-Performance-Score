from django.db.models import fields
from rest_framework import serializers
from .models import Product
from django.contrib.auth.models import User, Group

# Django Model 데이터를 Json 타입으로 바꿔주는(직렬화) 기능

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
