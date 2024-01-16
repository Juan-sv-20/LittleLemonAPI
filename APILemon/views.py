from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.core.paginator import Paginator, EmptyPage
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Category
from .serializers import CategorySerializer
# Create your views here.

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
        