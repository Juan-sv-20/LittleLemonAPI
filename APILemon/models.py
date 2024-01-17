from django.db import models
from django.contrib.auth.models import User, Group
import uuid
from django.conf import settings

# Create your models here.
class Category(models.Model):
    slug = models.SlugField(default=None)
    title = models.CharField(max_length=255)
    category_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    
    def __str__(self):
        return self.title

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField(default=100.00)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, related_name='products')
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    
    def __str__(self):
        return str(self.name)

class Cart(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.id)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True, related_name='cartitems')
    quantity = models.IntegerField(default=0)
    
    def __str__(self):
        return str(self.product)
    
class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed'),
    ]
    
    placed_at = models.DateTimeField(auto_now_add=True)
    pending_status = models.CharField(
        max_length = 50,
        choices = PAYMENT_STATUS_CHOICES,
        default = 'PAYMENT_STATUS_PENDING'
    )
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.PROTECT)
    delivery_crew = models.ForeignKey(User, on_delete=models.PROTECT, default=None, related_name='delivery_crew')
    
    def __str__(self):
        return self.pending_status + ' ' + self.owner.username

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    
    def __str__(self):
        return self.product.name