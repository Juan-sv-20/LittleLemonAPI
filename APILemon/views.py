from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission, SAFE_METHODS
from django.core.paginator import Paginator, EmptyPage
from rest_framework import status
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404

from .models import Category, Product, Cart, CartItem, Order, OrderItem
from .serializers import CartSerializer, CartItemSerializer, addCartitemSerializer, ProductSerializer, CategorySerializer, UserSerializer, OrderItemSerializer, OrderSerializer, CreateOrderSerializer, UpdateOrderSerializer

from django.contrib.auth.models import User, Group

from decimal import Decimal
# Create your views here.

""" def isStaff_Authenticated(request):
    if request.user.is_authenticated & request.user.is_staff:
        return True
    else:
        return False 
        
        #print(request.data['menuitem_id'])
        item = MenuItem.objects.get(pk=request.data['menuitem_id'])
        serializer_item = MenuItemSerializer(item)
        cart = Cart(user=user,menuitem=item,quantity=request.data['quantity'])
        serializer_cart = CartSerializer(data={
            'user': 1,
            'user_id' : 1,
            'menuitem' : 1,
            'menuitem_id' : 1, 
            'quantity': '5'})
        serializer_cart.is_valid()
        #serializer_cart.save()
        
        return Response(serializer_cart.data,status=status.HTTP_201_CREATED)

@api_view(['POST','GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def manager(request):
    if request.method == 'GET':
        users = User.objects.all()
        users = users.filter(groups__name='Manager')
            
        serializer_user = UserSerializer(users, many=True)
            
        return Response({'Managers' : serializer_user.data}, status=status.HTTP_200_OK)
    if request.method == 'POST':
        username = request.data['username']
    
        if username:
            user = get_object_or_404(User, username=username)
            serializer_user = UserSerializer(user)
            manager = Group.objects.get(name='Manager')
            manager.user_set.add(user)
            return Response(serializer_user.data, status=status.HTTP_201_CREATED)
        return Response({'message' : 'error'}, status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
def single_manager(request, id=None):  
    if id:
        user = get_object_or_404(User, pk=id)
        serializer_user = UserSerializer(user)
        manager = Group.objects.get(name='Manager')
        manager.user_set.remove(user)
        return Response(serializer_user.data, status=status.HTTP_200_OK)
    return Response({'message' : 'error'}, status.HTTP_400_BAD_REQUEST)

@api_view(['POST','GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def delivery_crew(request):
    if request.method == 'GET':
        users = User.objects.all()
        users = users.filter(groups__name='DeliveryCrew')
            
        serializer_user = UserSerializer(users, many=True)
            
        return Response({'DeliveryCrew' : serializer_user.data}, status=status.HTTP_200_OK)
    if request.method == 'POST':
        username = request.data['username']
    
        if username:
            user = get_object_or_404(User, username=username)
            serializer_user = UserSerializer(user)
            manager = Group.objects.get(name='DeliveryCrew')
            manager.user_set.add(user)
            return Response(serializer_user.data, status=status.HTTP_201_CREATED)
        return Response({'message' : 'error'}, status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
def single_delivery_crew(request, id=None):
    if id:
        user = get_object_or_404(User, pk=id)
        serializer_user = UserSerializer(user)
        manager = Group.objects.get(name='DeliveryCrew')
        manager.user_set.remove(user)
        return Response(serializer_user.data, status=status.HTTP_200_OK)
    return Response({'message' : 'error'}, status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
def menu_item(request):
    if request.method == 'GET':
        items = MenuItem.objects.select_related('category').all()
        
        category = request.query_params.get('category')
        to_price = request.query_params.get('to_price')
        search = request.query_params.get('search')
        ordering = request.query_params.get('ordering')
        
        perpage = request.query_params.get('perpage', default=10)
        page = request.query_params.get('page', default=1)
        
        if category:
            items = items.filter(category__title=category)
        if to_price:
            items = items.filter(price__lte=to_price)
        if search:
            items = items.filter(title__startwith=search)
        if ordering:
            ordering_fields = ordering.split(',')
            items = items.order_by(*ordering_fields)
        
        paginator = Paginator(items, per_page=perpage)
        try:
            items = paginator.page(number=page)
        except EmptyPage:
            items = []
        
        serializer_items = MenuItemSerializer(items, many=True)
        return Response(serializer_items.data)
    if request.method=='POST' and isStaff_Authenticated(request):
        serializer_items = MenuItemSerializer(data=request.data)
        serializer_items.is_valid(raise_exception=True)
        serializer_items.save()
        return Response(serializer_items.data, status.HTTP_201_CREATED)
    else:
        return Response({"message" : 'you do not have permission to this action'}, status.HTTP_403_FORBIDDEN)

@api_view(['GET','PUT','DELETE'])
def single_menu_item(request, id=None):
    item = get_object_or_404(MenuItem, pk=id)
    
    if request.method == 'GET':
        serializer_item = MenuItemSerializer(item)
        return Response(serializer_item.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        if isStaff_Authenticated(request):
            item = get_object_or_404(MenuItem, pk=id)
            
            serializer_item = MenuItemSerializer(item, data=request.data)
            serializer_item.is_valid(raise_exception=True)
            serializer_item.save()
            
            return Response(serializer_item.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'message' : 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
    elif request.method == 'DELETE':
        if isStaff_Authenticated(request):
            item = get_object_or_404(MenuItem, pk=id)
            item.delete()
            return Response({'message' : 'Menu Item was deleted succesfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'message' : 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
    
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def category(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        
        search = request.query_params.get('search')
        ordering = request.query_params.get('ordering')
        
        perpage = request.query_params.get('perpage', default=2)
        page = request.query_params.get('page', default=1)
        
        if search:
            categories = categories.filter(title__startwith=search)
        if ordering:
            ordering_fields = ordering.split(',')
            categories = categories.order_by(*ordering_fields)
        
        paginator = Paginator(categories, per_page=perpage)
        try:
            categories = paginator.page(number=page)
        except EmptyPage:
            categories = []
        
        serializer_categories = CategorySerializer(categories, many=True)
        return Response(serializer_categories.data, status.HTTP_200_OK)
        
    elif request.method == 'POST':
        serializer_category = CategorySerializer(data=request.data)
        serializer_category.is_valid(raise_exception=True)
        serializer_category.save()
        return Response(serializer_category.data, status.HTTP_201_CREATED)
    
@api_view(['GET', 'DELETE', 'PUT'])
@permission_classes([IsAuthenticated, IsAdminUser])
def single_category(request, id=None):
    if request.method == 'GET':
        category = get_object_or_404(Category,pk=id)
        serializer_category = CategorySerializer(category)
        return Response(serializer_category.data, status.HTTP_200_OK)
    if request.method == 'DELETE':
        category = get_object_or_404(Category, pk=id)
        category.delete()
        return Response({'message': 'Category was deleted succesfully'}, status.HTTP_200_OK)
    if request.method == "PUT":
        category = get_object_or_404(Category, pk=id)
        
        serializer_category = CategorySerializer(category, data=request.data)
        serializer_category.is_valid(raise_exception=True)
        serializer_category.save()
        
        return Response(serializer_category.data, status.HTTP_200_OK)
 """

@api_view(['POST','GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def manager(request):
    if request.method == 'GET':
        users = User.objects.all()
        users = users.filter(groups__name='Manager')
            
        serializer_user = UserSerializer(users, many=True)
            
        return Response({'Managers' : serializer_user.data}, status=status.HTTP_200_OK)
    if request.method == 'POST':
        username = request.data['username']
    
        if username:
            user = get_object_or_404(User, username=username)
            serializer_user = UserSerializer(user)
            manager = Group.objects.get(name='Manager')
            manager.user_set.add(user)
            return Response(serializer_user.data, status=status.HTTP_201_CREATED)
        return Response({'message' : 'error'}, status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
def single_manager(request, id=None):  
    if id:
        user = get_object_or_404(User, pk=id)
        serializer_user = UserSerializer(user)
        manager = Group.objects.get(name='Manager')
        manager.user_set.remove(user)
        return Response(serializer_user.data, status=status.HTTP_200_OK)
    return Response({'message' : 'error'}, status.HTTP_400_BAD_REQUEST)

@api_view(['POST','GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def delivery_crew(request):
    if request.method == 'GET':
        users = User.objects.all()
        users = users.filter(groups__name='DeliveryCrew')
            
        serializer_user = UserSerializer(users, many=True)
            
        return Response({'DeliveryCrew' : serializer_user.data}, status=status.HTTP_200_OK)
    if request.method == 'POST':
        username = request.data['username']
    
        if username:
            user = get_object_or_404(User, username=username)
            serializer_user = UserSerializer(user)
            manager = Group.objects.get(name='DeliveryCrew')
            manager.user_set.add(user)
            return Response(serializer_user.data, status=status.HTTP_201_CREATED)
        return Response({'message' : 'error'}, status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
def single_delivery_crew(request, id=None):
    if id:
        user = get_object_or_404(User, pk=id)
        serializer_user = UserSerializer(user)
        manager = Group.objects.get(name='DeliveryCrew')
        manager.user_set.remove(user)
        return Response(serializer_user.data, status=status.HTTP_200_OK)
    return Response({'message' : 'error'}, status.HTTP_400_BAD_REQUEST)

class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

class ProductViewSet(ModelViewSet):
    permission_classes = [(IsAuthenticated and IsAdminUser) | ReadOnly]
    
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    filter_backends= [SearchFilter, OrderingFilter]
    search_fields = ['name', 'description']
    pagination_class = PageNumberPagination

class CategoryViewSet(ModelViewSet):
    permission_classes = [(IsAuthenticated and IsAdminUser) | ReadOnly]
    
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    
    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk'])
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return addCartitemSerializer
        return CartItemSerializer
    def get_serializer_context(self):
        return {'cart_id' : self.kwargs['cart_pk']}

class CartViewSet(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    
    http_method_names = ['get', 'post', 'delete']
    
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    
class OrderViewSet(ModelViewSet):
    http_method_names = ['get','patch', 'post', 'delete', 'options', 'head']
    
    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(data=request.data, context={'user_id': self.request.user.id})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        elif self.request.method == 'PATCH':
            return UpdateOrderSerializer
        return OrderSerializer
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        elif user.groups.filter(name='DeliveryCrew').exists():
            return Order.objects.filter(delivery_crew=user)
        return Order.objects.filter(owner=user)