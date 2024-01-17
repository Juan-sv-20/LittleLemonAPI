from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

router = routers.DefaultRouter()

router.register('carts', views.CartViewSet)
router.register('products', views.ProductViewSet)
router.register('categories', views.CategoryViewSet)
router.register('orders', views.OrderViewSet, basename='orders')

cart_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
cart_router.register('items', views.CartItemViewSet, basename='cart-items')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(cart_router.urls)),
    path('groups/manager/users/', views.manager),
    path('groups/manager/users/<int:id>', views.single_manager),
    path('groups/delivery-crew/users/', views.delivery_crew),
    path('groups/delivery-crew/users/<int:id>', views.single_delivery_crew),
]