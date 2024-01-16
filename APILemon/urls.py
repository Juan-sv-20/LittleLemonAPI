from django.urls import path
from . import views

urlpatterns = [
    path('category/', views.category),
    path('category/<int:id>/', views.single_category),
]