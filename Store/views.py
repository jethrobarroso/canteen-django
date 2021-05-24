from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import *
from .serializers import *
# Create your views here.

class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all() 
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )


class MenuView(viewsets.ModelViewSet):
    queryset = Menu.objects.all() 
    serializer_class = MenuSerializer
    permission_classes = (permissions.IsAuthenticated, )


class OrderView(viewsets.ModelViewSet):
    queryset = Order.objects.all() 
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )


class LocationView(viewsets.ModelViewSet):
    queryset = Location.objects.all() 
    serializer_class = LocationSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )