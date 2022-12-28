from django.db import models
# from django.contrib.auth.models import User
#Imports
import random
import string

# Create your models here.

class Store(models.Model):
    store_name = models.CharField(max_length=100)
    store_address = models.CharField(max_length=100)
    store_manager = models.CharField(max_length=100)
    store_slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)
    store_image = models.ImageField(upload_to='store_images', blank=True)
    store_created = models.DateTimeField(blank=True,null=True)
    

    def __str__(self):
        return self.store_name

    def generate_code(self):
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return code


class Category(models.Model):
    category_name = models.CharField(max_length=100)
    category_slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)
    category_code = models.CharField(max_length=6, unique=True, null=True, blank=True)
    category_description = models.TextField(max_length=1000, blank=True)
    category_store = models.ForeignKey(Store, on_delete=models.CASCADE)
    category_created = models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return self.category_name


class Product(models.Model):
    product_name = models.CharField(max_length=100)
    product_slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)
    product_description = models.TextField(max_length=1000, blank=True)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_image = models.ImageField(upload_to='product_images', blank=True)
    product_category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    product_store = models.ForeignKey(Store, on_delete=models.CASCADE)
    product_created = models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return self.product_name

class Order(models.Model):
    order_id = models.CharField(max_length=100)
    order_date = models.DateTimeField(blank=True,null=True)
    order_products = models.ManyToManyField(Product)
    order_total = models.DecimalField(max_digits=10, decimal_places=2)
    order_store = models.ForeignKey(Store, on_delete=models.CASCADE)
    order_completed = models.BooleanField(default=False)
    order_created = models.DateTimeField(blank=True,null=True)


    def __str__(self):
        return self.order_id + ' - ' + self.order_store.store_name


class OrderItem(models.Model):
    order_item_id = models.CharField(max_length=100)
    order_item_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order_item_quantity = models.IntegerField()
    order_item_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_item_total = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    order_item_order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    order_item_created = models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return self.order_item_product.product_name


# class Transaction(models.Model):
#     transaction_number = models.CharField(max_length=100)
#     transaction_code = models.CharField(max_length=100)
#     transaction_date = models.DateTimeField(blank=True,null=True)
#     transaction_total = models.CharField(max_length=100)
#     transaction_order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     transaction_tax = models.CharField(max_length=100)
#     transaction_created = models.DateTimeField(blank=True,null=True)

#     def __str__(self):
#         return self.transaction_id


