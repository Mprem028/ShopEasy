

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, OrderItem
from products.models import Product
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse, HttpResponse
import json, csv
from django.core.paginator import Paginator
from django.contrib import messages
from orders.forms import CheckoutForm
import uuid
from django.shortcuts import render, get_object_or_404
from .models import Order



def cart_view(request):
    cart = request.session.get('cart', [])
    products = Product.objects.filter(id__in=cart)
    total = sum([p.price for p in products])

    return render(request, 'orders/cart.html', {
        'products': products,
        'total': total
    })



def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    
    # Convert product_id to string because keys in session dict are strings
    product_key = str(product_id)
    if product_key in cart:
        cart.pop(product_key)
        request.session['cart'] = cart
        request.session.modified = True
        messages.success(request, "Item removed from cart.")
    else:
        messages.error(request, "Item not found in your cart.")

    return redirect('orders:cart')



@login_required
def save_cart_session(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        if product_id:
            cart = request.session.get("cart", [])
            if product_id not in cart:
                cart.append(product_id)
            request.session["cart"] = cart
            messages.success(request, "Item added to cart!")
        return redirect("product_list")
    return redirect("product_list")

@login_required
def checkout_view(request):
    cart = request.session.get('cart', [])  # list of product IDs
    if not cart:
        messages.warning(request, "Your cart is empty.")
        return redirect('orders:cart')

    products = Product.objects.filter(id__in=cart)
    total = sum([p.price for p in products])

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # compose shipping address text
            addr_lines = [
                data['full_name'],
                data['address_line1'],
                data['address_line2'] or '',
                f"{data['city']}, {data['state']} {data['postal_code']}",
                data['country']
            ]
            shipping_text = "\n".join([line for line in addr_lines if line])

            payment_method = data['payment_method']  # 'COD' or 'CARD'

            # create order (payment_status pending initially)
            order = Order.objects.create(
                user=request.user,
                total=total,
                shipping_address=shipping_text,
                phone=data['phone'],
                payment_method=payment_method,
                payment_status='Pending',
                status='Pending',
            )

            # create order items (quantity default 1)
            for product in products:
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=1,
                    price=product.price
                )

            # If COD -> finalize order and clear cart
            if payment_method == 'COD':
                request.session['cart'] = []
                messages.success(request, "Order placed with Cash on Delivery.")
                return redirect('orders:order_success', pk=order.pk)

            # If CARD (fake) -> redirect to fake payment page
            return redirect('orders:fake_payment', pk=order.pk)
    else:
        # prefill form with user's name if available
        initial = {}
        if request.user.is_authenticated:
            initial['full_name'] = request.user.get_full_name() or request.user.username
        form = CheckoutForm(initial=initial)

    return render(request, 'orders/checkout.html', {
        'products': products,
        'total': total,
        'form': form
    })

@login_required
def fake_payment(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    if request.method == 'POST':
        # simulate payment success
        order.payment_status = 'Paid'
        order.transaction_id = str(uuid.uuid4())
        order.status = 'Processing'  # or whatever status you want after payment
        order.save()
        # clear cart in session (if not already)
        request.session['cart'] = []
        messages.success(request, "Payment successful (fake). Order placed.")
        return redirect('orders:order_success', pk=order.pk)

    return render(request, 'orders/fake_payment.html', {'order': order})

def payment_success(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'orders/payment_success.html', {'order': order})


@login_required
def order_success(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request,'orders/success.html', {'order':order})

def admin_check(user):
    return (
        user.is_authenticated and (
            user.is_superuser or
            user.is_staff or
            getattr(user, 'role', '') == 'admin'
        )
    )

@user_passes_test(admin_check, login_url='login')
def admin_orders(request):
    qs = Order.objects.all().order_by('-created_at')
    q = request.GET.get('q')
    if q:
        qs = qs.filter(id__icontains=q)
    paginator = Paginator(qs, 20)
    orders = paginator.get_page(request.GET.get('page',1))
    return render(request,'admin/orders_list.html', {'orders':orders})

@user_passes_test(admin_check, login_url='login')
def admin_order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        status = request.POST.get('status')
        note = request.POST.get('admin_notes')
        if status:
            order.status = status
        if note is not None:
            order.admin_notes = note
        order.save()
        messages.success(request, 'Order updated')
        return redirect('orders:admin_order_detail', pk=pk)
    return render(request,'admin/order_details.html', {'order':order})

@user_passes_test(admin_check, login_url='login')
def admin_export_csv(request):
    ids = request.GET.getlist('id')
    qs = Order.objects.filter(id__in=ids) if ids else Order.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="orders.csv"'
    writer = csv.writer(response)
    writer.writerow(['Order ID','User','Total','Status','Created','Shipping'])
    for o in qs:
        writer.writerow([o.id, o.user.email, float(o.total), o.status, o.created_at.isoformat(), str(o.shipping_address)])
    return response

@login_required(login_url='login')
def save_cart_session(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        # Store only product IDs for checkout
        request.session['cart'] = list(data.keys())
        request.session.modified = True
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})
