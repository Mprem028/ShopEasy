from django.urls import path
from . import views

urlpatterns = [
    # -------------------
    # Public (User) Routes
    # -------------------
    path('', views.product_list, name='product_list'),
    path('<slug:slug>/', views.product_detail, name='product_detail'),

    # -------------------
    # Admin Panel Routes
    # -------------------
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/products/', views.admin_products, name='admin_products'),
    path('admin/products/add/', views.admin_product_add, name='admin_product_add'),
    path('admin/products/edit/<int:pk>/', views.admin_product_edit, name='admin_product_edit'),
    path('admin/products/delete/<int:pk>/', views.admin_product_delete, name='admin_product_delete'),
]
