from django.urls import path
from . import views

urlpatterns = [
    path('category/', views.category),
    path('category/<int:id>/', views.single_category),
    path('menu-item/', views.menu_item),
    path('menu-item/<int:id>/', views.single_menu_item),
    path('groups/manager/users/', views.manager),
    path('groups/manager/users/<int:id>/', views.single_manager),
    path('groups/delivery-crew/users/', views.delivery_crew),
    path('groups/delivery-crew/users/<int:id>/', views.single_delivery_crew),
]