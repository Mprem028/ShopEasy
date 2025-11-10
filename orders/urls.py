from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # User cart and checkout
    path('cart/', views.cart_view, name='cart'),
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('save_cart_session/', views.save_cart_session, name='save_cart_session'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('fake-payment/<int:pk>/', views.fake_payment, name='fake_payment'),
    path('payment/success/<int:pk>/', views.payment_success, name='payment_success'),
    path('success/<int:pk>/', views.order_success, name='order_success'),

    # Admin routes
    path('admin/orders/', views.admin_orders, name='admin_orders'),
    path('admin/orders/<int:pk>/', views.admin_order_detail, name='admin_order_detail'),
    path('admin/orders/export/', views.admin_export_csv, name='admin_export_csv'),
]
