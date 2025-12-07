from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from .models import Product
from .forms import ProductForm
from orders.models import Order
from django.db.models import Sum



# ===========================
# USER VIEWS
# ===========================

def product_list(request):
    electronics = Product.objects.filter(category__icontains='Electronics', is_deleted=False)[:6]
    fashion = Product.objects.filter(category__icontains='Fashion', is_deleted=False)[:6]
    beauty = Product.objects.filter(category__icontains='Beauty', is_deleted=False)[:6]

    context = {
        'electronics': electronics,
        'fashion': fashion,
        'beauty': beauty,
    }
    return render(request, 'products/list.html', context)



def product_detail(request, slug):
    """Display details of a single product"""
    p = get_object_or_404(Product, slug=slug, is_deleted=False)
    return render(request, 'products/detail.html', {'product': p})

def home(request):
    if request.user.is_authenticated:
        # Redirect logged-in users directly to product list
        return redirect('product_list')
    return render(request, 'home.html')
# ===========================
# ADMIN CHECK
# ===========================

def admin_check(user):
    return user.is_authenticated and (user.is_superuser or getattr(user, 'role', '') == 'admin')



# ===========================
# ADMIN VIEWS
# ===========================

@user_passes_test(admin_check, login_url='login')
def admin_products(request):
    """Admin: list all products (including deleted)"""
    qs = Product.objects.all().order_by('-created_at')
    q = request.GET.get('q')
    if q:
        qs = qs.filter(name__icontains=q)

    paginator = Paginator(qs, 20)
    products = paginator.get_page(request.GET.get('page', 1))
    return render(request, 'admin/products_list.html', {'products': products})


@user_passes_test(admin_check, login_url='login')
def admin_product_add(request):
    """Admin: create a new product"""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Product created successfully!')
            return redirect('admin_products')
        else:
            messages.error(request, '⚠️ Error creating product. Please check the fields.')
    else:
        form = ProductForm()

    return render(request, 'admin/products_form.html', {'form': form, 'is_edit': False})


@user_passes_test(admin_check, login_url='login')
def admin_product_edit(request, pk):
    """Admin: edit existing product"""
    prod = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=prod)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Product updated successfully!')
            return redirect('admin_products')
        else:
            messages.error(request, '⚠️ Could not update product.')
    else:
        form = ProductForm(instance=prod)

    return render(request, 'admin/products_form.html', {
        'form': form,
        'is_edit': True,
        'prod': prod
    })


@user_passes_test(admin_check, login_url='login')
def admin_product_delete(request, pk):
    """Admin: soft delete a product (set is_deleted=True)"""
    prod = get_object_or_404(Product, pk=pk)
    # prod.is_deleted = True
    # prod.save()
    prod.delete()
    messages.warning(request, f'🗑 Product "{prod.name}" has been marked as deleted.')
    return redirect('admin_products')


@login_required(login_url='login')
@user_passes_test(admin_check, login_url='login')
def admin_dashboard(request):
    """Admin: dashboard metrics"""
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='Pending').count()
    total_products = Product.objects.filter(is_deleted=False).count()

    # Calculate revenue efficiently
    revenue = Order.objects.aggregate(total_amount=Sum('total'))['total_amount'] or 0


    context = {
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'total_products': total_products,
        'revenue': revenue
    }
    return render(request, 'admin/dashboard.html', context)
