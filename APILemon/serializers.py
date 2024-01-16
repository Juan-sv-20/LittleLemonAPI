from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Category, MenuItem, Cart, Order, OrderItem
from django.contrib.auth.models import User
import bleach

class CategorySerializer(serializers.ModelSerializer):
    def validate_slug(self, value):
        return bleach.clean(value)
    def validate_title(self, value):
        return bleach.clean(value)
    
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']

class MenuItemSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=255, validators = [UniqueValidator(queryset=MenuItem.objects.all())])
    price = serializers.DecimalField(max_digits=6, decimal_places=2)
    featured = serializers.BooleanField()
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    
    def validate_title(self, value):
        return bleach.clean(value)
    
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category', 'category_id']

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255, validators = [UniqueValidator(queryset=User.objects.all())])
    email = serializers.EmailField(max_length=255)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class CartSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    menuitem = MenuItemSerializer(read_only=True)
    menuitem_id = serializers.IntegerField(write_only=True)
    quantity = serializers.IntegerField()
    unit_price = serializers.SerializerMethodField(method_name='unitPrice')
    price = serializers.SerializerMethodField(method_name='price')
    
    class Meta:
        model = Cart
        fields = ['id', 'user', 'user_id', 'menuitem', 'menuitem_id', 'quantity', 'unit_price', 'price']
    
    def unitPrice(self, product=Cart):
        return MenuItem.objects.get(pk=product.menuitem_id).price
    
    def price(self, product=Cart):
        return product.unit_price * product.quantity
    
class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    delivery_crew = UserSerializer(read_only=True)
    delivery_crew_id = serializers.IntegerField(write_only=True)
    status = serializers.BooleanField()
    total = serializers.DecimalField(
        max_digits=6,
        decimal_places=2
    )
    date = serializers.DateField()
    
    class Meta:
        model = Order,
        fields = ['id', 'user', 'user_id', 'delivery_crew', 'delivery_crew_id', 'status', 'total', 'date']

class OrderItemSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)
    order_id = serializers.IntegerField(write_only=True)
    menuitem = MenuItemSerializer(read_only=True)
    menuitem_id = serializers.IntegerField(write_only=True)
    quantity = serializers.IntegerField()
    unit_price = serializers.SerializerMethodField(method_name='unitPrice')
    price = serializers.SerializerMethodField(method_name='price')
    
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'order_id', 'menuitem', 'menuitem_id', 'quantity', 'unit_price', 'price']
    
    def unitPrice(self, product=OrderItem):
        return MenuItem.objects.get(pk=product.menuitem_id).price
    
    def price(self, product=OrderItem):
        return product.unit_price * product.quantity