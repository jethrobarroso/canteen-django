from rest_framework import serializers
from .models import *

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta: 
        model = Category
        fields = ('id', 'url', 'description', 'slug', 'category_pic')


class MenuSerializer(serializers.HyperlinkedModelSerializer):
    class Meta: 
        model = Menu
        fields = ('id', 'url', 'name', 'description', 'category', 'price', 'food_pic', 'is_special')
        depth = 1


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta: 
        model = Category
        fields = ('id', 'url', 'fullname', 'phone_number', 'scheduled_for', 'status', 'payment', 'menu_items')


class LocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'url', 'name')
