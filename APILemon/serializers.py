from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Category, Product, Cart, CartItem, OrderItem, Order
from django.contrib.auth.models import User, Group
from django.db import transaction
import bleach
 
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
 
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_id', 'title', 'slug', 'products']
        depth=1

class CategoryProductSerializer(serializers.ModelSerializer):
    category_id = serializers.UUIDField()
    
    class Meta:
        model = Category
        fields = ['category_id']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description','price', 'category']
    category = CategoryProductSerializer
 
class CartItemSerializer(serializers.ModelSerializer):
    sub_total = serializers.SerializerMethodField(method_name='total')
    
    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'quantity', 'sub_total']
        depth=2
    
    def total(self, cartitem:CartItem):
        return cartitem.quantity * cartitem.product.price

class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    grand_total = serializers.SerializerMethodField(method_name='main_total')
    
    class Meta:
        model = Cart
        fields = ['id', 'items', 'grand_total']
        depth=1
    
    def main_total(self, cart:Cart):
        items = cart.items.all()
        total = sum([item.quantity * item.product.price for item in items])
        return total

class addCartitemSerializer(serializers.ModelSerializer):
    product_id = serializers.UUIDField()
    
    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError('There is no product associated with the given ID')
        return value
    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']
        
        try:
            cartitem = CartItem.objects.get(product_id=product_id, cart_id=cart_id)
            cartitem.quantity += quantity
            cartitem.save()
            
            self.instance = cartitem
        except:
            self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data)
        return self.instance
    
    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']

class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price']
     
class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    owner = UserSerializer(read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'placed_at', 'pending_status', 'owner', 'items']

class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()
    
    def validate_card_id(self, cart_id):
        if not Cart.objects.filter(pl=cart_id).exists():
            raise serializers.ValidationError('This cart_id is invalid')
        elif not CartItem.objects.filter(cart_id=cart_id).exists():
            raise serializers.ValidationError('Sorry your cart is empty')
        return cart_id
    
    def save(self, **kwargs):
        with transaction.atomic():
            cart_id = self.validated_data['cart_id']
            user_id = self.context['user_id']
            order = Order.objects.create(owner_id= user_id)
            cartitems = CartItem.objects.filter(cart_id=cart_id)
            orderitems = [
                OrderItem(
                    order = order,
                    product = item.product,
                    quantity = item.quantity
                )
                for item in cartitems
            ]
            OrderItem.objects.bulk_create(orderitems)
            return order
class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['pending_status']