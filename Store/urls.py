from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
# register paths for that view. 1st param is the name of resource in the url
router.register('categories', views.CategoryView)
router.register('menus', views.MenuView)
router.register('orders', views.OrderView)
router.register('locations', views.LocationView)

urlpatterns = [
    path('', include(router.urls))
]