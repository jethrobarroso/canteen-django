from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Category)
admin.site.register(Menu)
admin.site.register(OrderStatus)
admin.site.register(PaymentMethod)
admin.site.register(Location)
admin.site.register(Order)
admin.site.register(OrderItem)