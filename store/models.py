from django.db import models
# from django.contrib.auth.models import User
#Imports
import random
import string

# Create your models here.

class User(models.Model):
    user_name = models.CharField(max_length=100)
    user_email = models.EmailField(max_length=100)
    user_password = models.CharField(max_length=100)
    user_role = models.CharField(max_length=100)
    user_image = models.ImageField(upload_to='user_images', blank=True)
    user_created = models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return self.user_name

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

    @property
    def get_total_sales(self):
        total = 0
        for order in self.order_set.all():
            total += order.order_total
        return total

    @property
    def get_total_revenue(self):
        total = 0
        grand_total = 0
        for order in self.order_set.all():
            total += order.order_total
            grand_total = total * Setting.objects.all()[0].tax / 100
        return grand_total


class Category(models.Model):
    category_name = models.CharField(max_length=100)
    category_slug = models.SlugField(max_length=100, null=True, blank=True)
    category_code = models.CharField(max_length=6, unique=True, null=True, blank=True)
    category_description = models.TextField(max_length=1000, blank=True)
    category_store = models.ForeignKey(Store, on_delete=models.CASCADE)
    category_created = models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name_plural = 'Categories'


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
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    order_store = models.ForeignKey(Store, on_delete=models.CASCADE)
    order_completed = models.BooleanField(default=False)
    order_void = models.BooleanField(default=False)
    order_created = models.DateTimeField(blank=True,null=True)


    def __str__(self):
        return self.order_id + ' - ' + self.order_store.store_name


class OrderItem(models.Model):
    order_item_id = models.CharField(max_length=100)
    order_item_order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    order_item_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order_item_quantity = models.IntegerField()
    order_item_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_item_total = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    order_item_created = models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return self.order_item_product.product_name


class Transaction(models.Model):
    transaction_code = models.CharField(max_length=100)
    transaction_date = models.DateTimeField(blank=True,null=True)
    transaction_total = models.CharField(max_length=100)
    transaction_order = models.ForeignKey(Order, on_delete=models.CASCADE)
    transaction_tax = models.CharField(max_length=100)
    transaction_created = models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return self.transaction_code



class Setting(models.Model):
    CURRENCY = [
        ('USD', 'USD'),
        ('EUR', 'EUR'),
        ('CNY', 'CNY'),
        ('JPY', 'JPY'),
        ('PHP', 'PHP'),
    ]
    setting_id = models.CharField(max_length=100)
    tax = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=100, null=True, blank=True, choices=CURRENCY)
    setting_created = models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return self.setting_id

STOCKS = [
    ('In Stock', 'In Stock'),
    ('Out of Stock', 'Out of Stock'),
]

class Inventory(models.Model):
    inventory_id = models.CharField(max_length=100)
    inventory_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    inventory_stocks = models.IntegerField()
    inventory_status = models.CharField(max_length=100, null=True, blank=True, choices=STOCKS, default='In Stock')
    inventory_created = models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return self.inventory_id

    class Meta:
        verbose_name_plural = 'Inventories'




