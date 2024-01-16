from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.core.paginator import Paginator, EmptyPage
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Category, MenuItem
from .serializers import CategorySerializer, MenuItemSerializer

from django.contrib.auth.models import User, Group
# Create your views here.

def isStaff_Authenticated(request):
    if request.user.is_authenticated & request.user.is_staff:
        return True
    else:
        return False

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def manager(request):
    pass

@api_view(['GET','DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
def single_manager(request):
    pass

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def delivery_crew(request):
    pass

@api_view(['GET','DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
def single_delivery_crew(request):
    pass

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
        