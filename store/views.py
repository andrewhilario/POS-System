from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Store, Category, Product, Order, OrderItem
from django.contrib import messages
from django.utils import timezone
from uuid import uuid4
from django.utils.text import Truncator
#Imports



# Create your views here.
def dashboard(request):
    return render(request, 'includes/dashboard.html')

def store_list (request):
    stores = Store.objects.all()
    context = {
        'stores': stores
    }

    return render(request, 'includes/storelist.html', context)

def delete_store(request, id):
    store = get_object_or_404(Store, id=id)
    store.delete()
    messages.success(request, 'Store deleted successfully')
    return redirect('store_list')

def add_store(request):
    if request.method == 'POST' and request.FILES:
        store_name = request.POST.get('store-name')
        store_address = request.POST.get('store-address')
        store_manager = request.POST.get('store-manager')
        store_image = request.FILES.get('store-image')

        print(store_name, store_address, store_manager, store_image)

        store_obj = Store.objects.create(
            store_name=store_name,
            store_address=store_address,
            store_manager=store_manager,
            store_image=store_image
        )
        store_obj.save()
        messages.success(request, 'Store added successfully')


    return render(request, 'includes/addstore.html')

def edit_store(request, id):
    store = get_object_or_404(Store, id=id)
    if request.method == 'POST' and request.FILES:
        store.store_name = request.POST.get('store-name')
        store.store_address = request.POST.get('store-address')
        store.store_manager = request.POST.get('store-manager')
        store.store_image = request.FILES.get('store-image')
        store.store_slug = request.POST.get('store-slug')

        store.save()
        messages.success(request, 'Store updated successfully')
        return redirect('store_list')

    context = {
        'store': store
    }
    return render(request, 'includes/editstore.html', context)


def pos_dashboard(request, store_slug):
    store = get_object_or_404(Store, store_slug=store_slug)
    context = {
        'store': store
    }
    return render(request, 'includes/pos/pos_includes/pos_dashboard.html', context)

def pos_categories(request, store_slug):
    store = get_object_or_404(Store, store_slug=store_slug)
    category = Category.objects.filter(category_store=store)

    context = {
        'store': store,
        'category': category
    }
    return render(request, 'includes/pos/pos_includes/pos_categories.html', context)

def add_category(request, store_slug):
    store = get_object_or_404(Store, store_slug=store_slug)
    if request.method == 'POST':
        category_name = request.POST.get('category-name')
        category_slug = request.POST.get('category-slug')
        category_code = request.POST.get('category-code')
        category_description = request.POST.get('category-description')
        # category_store = request.POST.get('category-store')

        if Category.objects.filter(category_name=category_name).exists():
            messages.error(request, 'Category already exists')
            return redirect('add_category' , store_slug=store_slug)
        else:
            category_obj = Category.objects.create(
                category_name=category_name,
                category_store=store,
                category_slug=category_slug,
                category_code=category_code,
                category_description=category_description,
                category_created=timezone.now()
            )
            category_obj.save()
            print(category_name,category_slug,category_code, category_description)
            messages.success(request, 'Category added successfully')
            return redirect('pos_categories', store_slug=store_slug)

    context = {
        'store': store
    }
    return render(request, 'includes/pos/pos_includes/pos_add_category.html', context)

def update_category(request, store_slug, pk):
    store = get_object_or_404(Store, store_slug=store_slug)
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category_name = request.POST.get('category-name')
        category_slug = request.POST.get('category-slug')
        category_code = request.POST.get('category-code')
        category_description = request.POST.get('category-description')
        # category_store = request.POST.get('category-store')

        if Category.objects.filter(category_name=category_name).exists():
            messages.error(request, 'Category already exists')
            return redirect('update_category' , store_slug=store_slug)
        else:
            Category.objects.filter(pk=pk).update(
                category_name=category_name,
                category_store=store,
                category_slug=category_slug,
                category_code=category_code,
                category_description=category_description,
                category_created=timezone.now()
            )


            messages.success(request, 'Category added successfully')
            return redirect('pos_categories', store_slug=store_slug)

    context = {
        'store': store
    }
    return render(request, 'includes/pos/pos_includes/pos_update_category.html', context)

def delete_category(request, store_slug, pk):
    store = get_object_or_404(Store, store_slug=store_slug)
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, 'Category deleted successfully')
    return redirect('pos_categories', store_slug=store_slug)


def pos(request, store_slug):
    store = get_object_or_404(Store, store_slug=store_slug)
    ctg = Category.objects.filter(category_store=store)
    product = Product.objects.filter(product_store=store)
    order = Order.objects.filter(order_store=store)
    order_item = OrderItem.objects.filter(order_item_product__product_store=store)

    order = Order.objects.filter(order_store=store)
    for o in order:
        order_completed = o.order_completed
        print(o.order_products.all(), 'This is all the products')

    sort = request.GET.get('sort', None)
    category = request.GET.get('filter', None)

    order = []
    if sort == 'new':
        order.append('-product_created')
    elif sort == 'old':
        order.append('product_created')
    elif sort == 'price_desc':
        order.append('-product_price')
    elif sort == 'price_asc':
        order.append('product_price')

    if category and category != 'all':
        category = category.replace('-', ' ')
        product = product.filter(product_category__category_name=category)

    if order:
        product = product.order_by(*order)

    category = Category.objects.order_by('category_name').values('category_name').distinct()


    context = {
        'store': store,
        'category': category,
        'products': product,
        'order_items': order_item,
        'order': order_completed        
    }
    return render(request, 'includes/pos/pos_includes/pos.html', context)


def add_order(request, store_slug, pk):
    store = get_object_or_404(Store, store_slug=store_slug)
    category = Category.objects.filter(category_store=store)
    product = Product.objects.filter(id=pk)

    uuid = uuid4()

    truncate_uuid = str(uuid)[:6]
    print(truncate_uuid)

    if request.method == 'POST':
        if(request.POST.get('order-modal-qty') == ''):
            messages.error(request, 'Please enter a quantity')
            return redirect('pos', store_slug=store_slug)
        else:
            for p in product:
                order_product = p
                order_quantity = request.POST.get('order-modal-qty')
                order_price = p.product_price

                orderItem_obj = OrderItem.objects.create(
                    order_item_id=truncate_uuid,
                    order_item_product=order_product,
                    order_item_quantity=order_quantity,
                    order_item_price=order_price,
                    order_item_total=float(order_quantity) * float(order_price),
                    order_item_created=timezone.now()
                )
                orderItem_obj.save()

                messages.success(request, 'Order added successfully')
                return redirect('pos', store_slug=store_slug)

    context = {
        'store': store,
        'category': category,
        'products': product        
    }
    return redirect('pos', store_slug=store_slug)

def update_order(request, store_slug, pk):
    store = get_object_or_404(Store, store_slug=store_slug)
    order = get_object_or_404(OrderItem, pk=pk)


    if request.method == 'POST':
        order_quantity = request.POST.get('order-qty')
        order_product = request.POST.get('order-product')


        if Product.objects.filter(product_name=order_product).exists():
            print('product exists')
            if order_product == '':
                messages.error(request, 'Please enter a product')
                return redirect('update_order', store_slug=store_slug, pk=pk)
            elif order_quantity == '':
                messages.error(request, 'Please enter a quantity')
                return redirect('update_order', store_slug=store_slug, pk=pk)
            else:
                product = Product.objects.get(product_name=order_product)
                order_price = product.product_price

                OrderItem.objects.filter(pk=pk).update(
                    order_item_quantity=order_quantity,
                    order_item_product=product,
                    order_item_price=order_price,
                    order_item_total=float(order_quantity) * float(order_price),
                    order_item_created=timezone.now()
                )
        else: 
            messages.error(request, 'Product does not exist')
            return redirect('update_order', store_slug=store_slug, pk=pk)
        
        messages.success(request, 'Order updated successfully')
        return redirect('pos', store_slug=store_slug)



    context = {
        'store': store,
        'order': order
    }
    return render(request, 'includes/pos/pos_includes/pos_edit_order.html', context)

def delete_order(request, store_slug, pk):
    store = get_object_or_404(Store, store_slug=store_slug)
    order = get_object_or_404(OrderItem, pk=pk)
    order.delete()
    messages.success(request, 'Order deleted successfully')
    return redirect('pos', store_slug=store_slug)

def pos_orders(request, store_slug):
    store = get_object_or_404(Store, store_slug=store_slug)
    order_item = OrderItem.objects.filter(order_item_product__product_store=store)

    order_total = 0
    for o in order_item:
        order_total += o.order_item_total

    context = {
        'store': store,
        'order_items': order_item,
        'order_total': order_total
    }
    return render(request, 'includes/pos/pos_includes/pos_orders.html', context)

def pos_getOrders(request, store_slug):
    store = get_object_or_404(Store, store_slug=store_slug)
    order_item = OrderItem.objects.filter(order_item_product__product_store=store)
    
    uuid = uuid4()

    truncate_uuid = str(uuid)[:7]



    order_total = 0
    for o in order_item:
        order_total += o.order_item_total

    products = OrderItem.objects.filter(order_item_product__product_store=store).values('order_item_product_id')
    products = Product.objects.filter(id__in=products)
    print(products)


    order_obj = Order.objects.create(
        order_id=truncate_uuid,
        order_date=timezone.now(),
        order_total=order_total,
        order_store=store,
        order_completed=True,
        order_created=timezone.now()
    )
    order_obj.order_products.set(products)
    order_obj.save()
    messages.success(request, 'Order completed successfully')

    return redirect('pos', store_slug=store_slug)



def pos_sales(request, store_slug):
    store = get_object_or_404(Store, store_slug=store_slug)
    context = {
        'store': store
    }
    return render(request, 'includes/pos/pos_includes/pos_sales.html', context)

def pos_products(request, store_slug):
    store = get_object_or_404(Store, store_slug=store_slug)
    product = Product.objects.filter(product_store=store)
    context = {
        'store': store,
        'products': product
    }
    return render(request, 'includes/pos/pos_includes/pos_products.html', context)

def add_product(request, store_slug):
    store = get_object_or_404(Store, store_slug=store_slug)
    category = Category.objects.filter(category_store=store)
    print(request.POST, request.FILES)
    if request.method == 'POST' and request.FILES:
        product_name = request.POST.get('product-name')
        product_slug = request.POST.get('product-slug')
        product_description = request.POST.get('product-description')
        product_category = request.POST.get('product-category')
        product_price = request.POST.get('product-price')
        product_image = request.FILES.get('product-image')
        # product_store = request.POST.get('product-store')

        if Product.objects.filter(product_name=product_name).exists():
            messages.error(request, 'Product already exists')
            return redirect('add_product' , store_slug=store_slug)
        else:
            category = Category.objects.get(pk=product_category)
            product_obj = Product.objects.create(
                product_name=product_name,
                product_store=store,
                product_slug=product_slug,
                product_description=product_description,
                product_category=category,
                product_price=product_price,
                product_image=product_image,
                product_created=timezone.now()
            )
            product_obj.save()

            messages.success(request, 'Product added successfully')
            return redirect('pos_products', store_slug=store_slug)



    context = {
        'store': store,
        'category': category
    }
    return render(request, 'includes/pos/pos_includes/pos_add_product.html', context)


def update_product(request, store_slug, pk):
    store = get_object_or_404(Store, store_slug=store_slug)
    product = get_object_or_404(Product, pk=pk)
    category = Category.objects.filter(category_store=store)
    if request.method == 'POST':
        product_name = request.POST.get('product-name')
        product_slug = request.POST.get('product-slug')
        product_description = request.POST.get('product-description')
        product_category = request.POST.get('product-category')
        product_price = request.POST.get('product-price')
        product_image = request.FILES.get('product-image')
        # product_store = request.POST.get('product-store')

        if Product.objects.filter(product_name=product_name).exists():
            messages.error(request, 'Product already exists')
            return redirect('update_product' , store_slug=store_slug)
        else:
            category = Category.objects.get(pk=product_category)
            # Product.objects.filter(pk=pk).update(
            #     product_name=product_name,
            #     product_store=store,
            #     product_slug=product_slug,
            #     product_description=product_description,
            #     product_category=category,
            #     product_price=product_price,
            #     product_image=product_image,
            #     product_created=timezone.now()
            # )

            messages.success(request, 'Product added successfully')
            return redirect('pos_products', store_slug=store_slug)

    context = {
        'store': store,
        'category': category,
        'product': product
    }
    return render(request, 'includes/pos/pos_includes/pos_update_product.html', context)

def delete_product(request, store_slug, pk):
    store = get_object_or_404(Store, store_slug=store_slug)
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    messages.success(request, 'Product deleted successfully')
    return redirect('pos_products', store_slug=store_slug)


def pos_customers(request, store_slug):
    store = get_object_or_404(Store, store_slug=store_slug)
    context = {
        'store': store
    }
    return render(request, 'includes/pos/pos_includes/pos_customers.html', context)

def pos_messages(request, store_slug):
    store = get_object_or_404(Store, store_slug=store_slug)
    context = {
        'store': store
    }
    return render(request, 'includes/pos/pos_includes/pos_messages.html', context)