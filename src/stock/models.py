"""
Defines essential fields for the model and
behavior for data that is stored.
Each model maps to a single database table
"""

from django.db import models


ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('refunded', 'Refunded')
)


class Store(models.Model):
    store_id = models.PositiveIntegerField(primary_key=True)
    contact_email = models.EmailField()

    class Meta:
        db_table = 'store'


class Category(models.Model):
    category_id = models.PositiveIntegerField(primary_key=True)
    category_name = models.CharField(max_length=50)
    subcategory_name = models.CharField(max_length=50, blank=True)

    class Meta:
        db_table = 'category'


class Product(models.Model):
    product_id = models.PositiveIntegerField(primary_key=True)
    product_name = models.CharField(max_length=50)
    product_price = models.PositiveIntegerField(default=0)
    store_id = models.ForeignKey(Store, on_delete='CASCADE')
    category_id = models.ForeignKey(Category, on_delete='CASCADE')
    quantity_available = models.IntegerField(default=0)

    class Meta:
        db_table = 'product'


class Barcode(models.Model):
    product_id = models.ForeignKey(Product, on_delete='CASCADE')
    barcode_id = models.CharField(max_length=13)

    class Meta:
        db_table = 'barcode'


class Supplier(models.Model):
    supplier_id = models.PositiveIntegerField(primary_key=True)
    supplier_name = models.CharField(max_length=50)
    contact_phone = models.CharField(max_length=12)
    contact_email = models.EmailField()

    class Meta:
        db_table = 'supplier'


class Order(models.Model):
    product_id = models.ForeignKey(Product, on_delete='CASCADE')
    order_id = models.PositiveIntegerField(primary_key=True)
    order_date = models.DateField(auto_now_add=True)
    quantity = models.PositiveIntegerField()
    order_delivery_date = models.DateField()
    order_status = models.CharField(max_length=50, default='created', choices=ORDER_STATUS_CHOICES)
    supplier_id = models.ForeignKey(Supplier, on_delete='CASCADE')

    class Meta:
        db_table = 'order'
