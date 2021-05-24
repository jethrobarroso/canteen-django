from datetime import datetime
import os
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import BLANK_CHOICE_DASH
from django.urls import reverse
from django.dispatch import receiver
from django_resized import ResizedImageField
from django.utils.text import slugify
from django_extensions.db.fields import AutoSlugField
# from rest_framework import serializers


def food_pic_file_name(instance, filename):
    return "/".join(["food_pictures", str(instance.id), filename])


def category_pic_file_name(instance, filename):
    return "/".join(["category_pictures", str(instance.id), filename])


class Category(models.Model):
    description = models.CharField(max_length=240, unique=True)
    slug = AutoSlugField(populate_from='description')
    category_pic = ResizedImageField(size=[300,200], quality=100, crop=['middle', 'center'],
        upload_to=category_pic_file_name, default='no-image.jpg'
    )

    def save(self, file_changed=False, *args, **kwargs):
        self.slug = slugify(self.description)

        if self.pk is None:
            saved_image = self.category_pic
            self.category_pic = None
            super().save(*args, **kwargs)
            self.category_pic = saved_image
            kwargs.pop("force_insert", None)

        dir = f"media/category_pictures/{self.pk}"
        # Remove all files if image was updated
        if file_changed and os.path.exists(dir):
            for file in os.scandir(dir):
                os.remove(file.path)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.description


class Menu(models.Model):
    name = models.CharField(max_length=240)
    description = models.TextField(max_length=240, blank=True, null=True)
    category = models.ForeignKey(Category, models.SET_NULL, blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    food_pic = ResizedImageField(size=[300,200], quality=100, crop=['middle', 'center'],
        upload_to=food_pic_file_name, null=True, blank=True)
    is_special = models.BooleanField(default=False)

    def save(self, file_changed=False, *args, **kwargs):
        if self.pk is None:
            saved_image = self.food_pic
            self.food_pic = None
            super().save(*args, **kwargs)
            self.food_pic = saved_image
            kwargs.pop("force_insert", None)

        dir = f"media/food_pictures/{self.pk}"
        # Remove all files if image was updated
        if file_changed and os.path.exists(dir):
            for file in os.scandir(dir):
                os.remove(file.path)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class OrderStatus(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class PaymentMethod(models.Model):
    name = models.CharField(max_length=250, unique=True)
    
    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=250, unique=True)
    
    def __str__(self):
        return self.name


def default_status():
    return OrderStatus.objects.get(name="Created")

def default_payment():
    return PaymentMethod.objects.get(name="Cash")

def default_location():
    return Location.objects.get(name="Office")


class Order(models.Model):
    fullname = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    location = models.ForeignKey(Location, models.SET_DEFAULT, 
        default=default_location)
    scheduled_for = models.DateTimeField()
    status = models.ForeignKey(OrderStatus, models.SET_DEFAULT, 
        default=default_status)
    payment = models.ForeignKey(PaymentMethod, models.SET_DEFAULT,
        default=default_payment)
    menu_items = models.ManyToManyField(Menu, through='OrderItem')

    def __str__(self):
        return f'Order: {self.fullname}, {self.phone_number}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=CASCADE)
    menu = models.ForeignKey(Menu, on_delete=CASCADE)
    qty = models.IntegerField(default=1)

    class Meta:
        unique_together = [['order', 'menu']]


@receiver(models.signals.post_delete, sender=Menu)
def auto_delete_file_on_delete(sender, instance, **kwargs):

    if instance.food_pic:
        if os.path.isfile(instance.food_pic.path):
            os.remove(instance.food_pic.path)
