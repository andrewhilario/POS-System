from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Store, Category, Product, Order, OrderItem, Transaction, Setting, Inventory
from django.contrib import messages
from django.utils import timezone
from uuid import uuid4
from django.utils.text import Truncator
from django.db.models import Count, Sum, F
#Imports



# Create your views here.
def dashboard(request):
    stores = Store.objects.all()
    settings = Setting.objects.all()
    order = Order.objects.all()
    order_item = OrderItem.objects.all()

    for setting in settings:
        currency = setting.currency

    ord_total = 0
    for o in order:
        ord_total += o.order_total
        order_revenue = ord_total * setting.tax / 100
        print(ord_total)

    
    order_items = 0
    for item in order_item:
        order_items += item.order_item_quantity
    print(order_items)


    for store in stores:
        store_total_sales = store.get_total_sales
        store_total_revenue = store.get_total_revenue
        print(store_total_revenue)

    context = {
        'stores': stores,
        'currency': currency,
        'store_total_sales': store_total_sales,
        'order_total': ord_total,
        'order_revenue': order_revenue,
        'order_items': order_items,
    }
    return render(request, 'includes/dashboard.html', context)

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
        store_slug = request.POST.get('store-slug')

        print(store_name, store_address, store_manager, store_image)

        store_obj = Store.objects.create(
            store_name=store_name,
            store_address=store_address,
            store_manager=store_manager,
            store_image=store_image,
            store_slug=store_slug
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
    order = Order.objects.filter(order_store=store)
    settings = Setting.objects.all()

    #Settings
    for s in settings:
        tax = s.tax
        tax = tax / 100
        currency = s.currency

    #Dashboard Functionality
    total_sales = 0
    total_revenue = 0
    estimated_sales_per_day = 5000
    estimated_revenue_per_day = 2500
    product = None

    
    total_sales = sum([o.order_total for o in order])
    total_revenue = sum([o.order_total for o in order]) * tax
    # print(total_sales)
    # print(total_revenue)


    percentage_sales = (total_sales / estimated_sales_per_day) * 100
    # print(percentage_sales)
    percentage_revenue = (total_revenue / estimated_revenue_per_day) * 100
    # print(percentage_revenue)

    #Get the total quantity of products sold
    total_quantity = 0
    for o in order:
        for i in o.orderitem_set.all():
            total_quantity += i.order_item_quantity

    # print(total_quantity, "qty")

    #Get the quantity of a specific product sold
    product_list = Order.objects.filter(order_store=store).values_list('orderitem__order_item_product__product_name').annotate(total=Sum('orderitem__order_item_quantity')).order_by('-total')[:4]

    most_sold_product= []
    most_sold_qty = []
    for product in product_list:
        most_sold_product.append(product[0])
        most_sold_qty.append(product[1])
    #Sales per month
    sales_per_month = []
    for i in range(1, 13):
        sales_per_month.append(sum([o.order_total for o in order if o.order_created.month == i]))

    #Revenue per month
    revenue_per_month = []
    for i in range(1, 13):
        revenue_per_month.append(sum([o.order_total for o in order if o.order_created.month == i]) * tax)
    
    # print(sales_per_month)
    # print(revenue_per_month)



    context = {
        'store': store,
        'orders': order,
        'tax': tax,
        'currency': currency,
        'total_sales': total_sales,
        'total_revenue': total_revenue,
        'estimated_sales_per_day': estimated_sales_per_day,
        'estimated_revenue_per_day': estimated_revenue_per_day,
        'percentage_sales': percentage_sales,
        'percentage_revenue': percentage_revenue,
        'revenue_per_month': revenue_per_month,
        'sales_per_month': sales_per_month,
        'total_quantity': total_quantity,
        'most_sold_product': most_sold_product,
        'most_sold_qty': most_sold_qty,
        'products': product
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

        if Category.objects.filter(category_store=store, category_name=category_name).exists():
            messages.error(request, 'Category already exists')
            return redirect('pos_categories', store_slug=store_slug)
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
    order_items = OrderItem.objects.filter(order_item_product__product_store=store)
    settings = Setting.objects.all()

    for setting in settings:
        currency = setting.currency

    order_item = OrderItem.objects.filter(order_item_product__product_store=store, order_item_order__order_completed=False)
    order_completed = False

    for ord in order:
        order_completed = ord.order_completed
    print(order_completed)

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
        'order_completed': order_completed,
        'currency': currency
    }
    return render(request, 'includes/pos/pos_includes/pos.html', context)


def add_order(request, store_slug, pk):
    store = get_object_or_404(Store, store_slug=store_slug)
    # category = Category.objects.filter(category_store=store)
    product = Product.objects.filter(id=pk)
    uuid = uuid4()
    truncate_uuid = str(uuid)[:6]
    print(truncate_uuid)

    if request.method == 'POST':
        quantity = request.POST.get('order-modal-qty')
        if(quantity == ''):
            messages.error(request, 'Please enter a quantity')
            return redirect('pos', store_slug=store_slug)
        else:
            order_obj = None
            if Order.objects.filter(order_completed=False).exists():
                order_obj = Order.objects.get(order_completed=False)
                print(order_obj.id)
                print('Order Exists')
                for prd,qty in zip(product,quantity):
                    order_item_obj = OrderItem.objects.create(
                        order_item_id=truncate_uuid,
                        order_item_order=order_obj,
                        order_item_product=prd,
                        order_item_quantity=qty,
                        order_item_price=prd.product_price,
                        order_item_total=float(prd.product_price) * float(qty),
                        order_item_created=timezone.now()
                    )
                    order_item_obj.save()

            else:
                print('Order Created')
                order_obj = Order.objects.create(
                    order_id=truncate_uuid,
                    order_store=store,
                    order_completed=False,
                    order_created=timezone.now()
                )
                order_obj.save()
                for prd,qty in zip(product,quantity):
                    order_item_obj = OrderItem.objects.create(
                        order_item_id=truncate_uuid,
                        order_item_order=order_obj,
                        order_item_product=prd,
                        order_item_quantity=qty,
                        order_item_price=prd.product_price,
                        order_item_total=float(prd.product_price) * float(qty),
                        order_item_created=timezone.now()
                    )
                    order_item_obj.save()


            messages.success(request, 'Order added successfully')
            return redirect('pos', store_slug=store_slug)

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
    order_item = OrderItem.objects.filter(order_item_product__product_store=store, order_item_order__order_completed=False)
    order = Order.objects.filter(order_store=store, order_completed=False)
    settings = Setting.objects.all()

    order_total = 0
    for o in order_item:
        order_total += o.order_item_total
        print(o, "This is the order item")
        

    for setting in settings:
        tax = setting.tax
        currencies = setting.currency
        tax = float(tax) / 100
        print(tax)

    order_completed = True
    order_date = None
    order_id = None
    for ord in order:
        order_completed = ord.order_completed
        order_date = ord.order_created
        order_id = ord.order_id

    context = {
        'store': store,
        'order_items': order_item,
        'order_total': order_total,
        'order_completed': order_completed,
        'order_date': order_date,
        'order_id': order_id,
        'tax': tax,
        'currencies': currencies
    }
    return render(request, 'includes/pos/pos_includes/pos_orders.html', context)

def pos_getOrders(request, store_slug):
    store = get_object_or_404(Store, store_slug=store_slug)
    order = Order.objects.filter(order_store=store, order_completed=False)
    order_item = OrderItem.objects.filter(order_item_order__in=order)
    settings = Setting.objects.all()

    for setting in settings:
        tax = setting.tax
        tax = float(tax) / 100
        print(tax)


    order_total = 0
    for o in order_item:
        print(o, "This is the order item")
        order_total += o.order_item_total
        order_quantity = o.order_item_quantity

        print(order_quantity, "This is the order quantity")

    ord = None  
    for ord in order:
        order_ttl = ord.order_total
        print(order_ttl)


    Order.objects.filter(order_store=store, order_completed=False).update(
        order_total=order_total,
        order_date=timezone.now(),
        order_completed=True
    )
    uuid = uuid4()
    truncate_uuid = str(uuid)[:4]
    truncate_uuid = truncate_uuid.upper()
    transaction_obj = Transaction.objects.create(
        transaction_code="CODE" + truncate_uuid,
        transaction_date=timezone.now(),
        transaction_total=order_total,
        transaction_order=ord,
        transaction_tax=float(order_total) * float(tax),
        transaction_created=timezone.now(),
    )
    transaction_obj.save()
    for o in order_item:
        Inventory.objects.filter(inventory_product=o.order_item_product).update(
            inventory_stocks=F('inventory_stocks') - o.order_item_quantity
        )
    
    messages.success(request, 'Order completed successfully')
    return redirect('pos', store_slug=store_slug)

def pos_sales(request, store_slug):
    store = get_object_or_404(Store, store_slug=store_slug)
    order = Order.objects.filter(order_store=store, order_completed=True)
    settings = Setting.objects.all()

    for setting in settings:
        tax = setting.tax
        currencies = setting.currency
        tax = float(tax) / 100
        print(tax)

    order_completed = False
    for ord in order:
        order_completed = ord.order_completed
        print(order_completed)

    transaction = Transaction.objects.filter(transaction_order__order_completed=True)


    context = {
        'store': store,
        'orders': order,
        'order_completed': order_completed,
        'transactions': transaction,
        'tax': tax,
        'currencies': currencies
    }
    return render(request, 'includes/pos/pos_includes/pos_sales.html', context)

def pos_getReceipt(request, store_slug, pk):
    store = get_object_or_404(Store, store_slug=store_slug)
    transaction = get_object_or_404(Transaction, pk=pk)
    order = Order.objects.filter(order_store=store, order_completed=True)

    for ord in order:
        order_id = ord.order_id
    order_item = OrderItem.objects.filter(order_item_order=transaction.transaction_order, order_item_order__order_completed=True)
    settings = Setting.objects.all()

    print(transaction.transaction_order)
    for setting in settings:
        tax = setting.tax
        currencies = setting.currency
        tax = float(tax) / 100


    order_completed = False
    order_date = None
    order_id = None
    
    for orderItem in order_item:
        order_completed = orderItem.order_item_order.order_completed
        order_date = orderItem.order_item_order.order_date
        order_id = orderItem.order_item_order.order_id
        order_total = orderItem.order_item_order.order_total


    context = {
        'store': store,
        'transaction': transaction,
        'order_items': order_item,
        'order_completed': order_completed,
        'order_date': order_date,
        'order_id': order_id,
        'order_total': order_total,
        'tax': tax,
        'currencies': currencies
    }
    return render(request, 'includes/pos/pos_includes/receipt.html', context)

def pos_deleteReceipt(request, store_slug, pk):
    store = get_object_or_404(Store, store_slug=store_slug)
    transaction = get_object_or_404(Transaction, pk=pk)
    transaction.delete()
    messages.success(request, 'Receipt deleted successfully')
    return redirect('pos_sales', store_slug=store_slug)


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
        product_stocks = request.POST.get('product-stocks')
        product_price = request.POST.get('product-price')
        product_image = request.FILES.get('product-image')
        # product_store = request.POST.get('product-store')

        if Product.objects.filter(product_name=product_name).exists():
            messages.error(request, 'Product already exists')
            return redirect('add_product' , store_slug=store_slug)
        else:
            category = Category.objects.get(pk=product_category)
            print(request.POST, request.FILES)
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

            uuid = uuid4()
            truncate_uuid = str(uuid)[:5]
            truncate_uuid = truncate_uuid.upper()

            
            inventory_obj = Inventory.objects.create(
                inventory_id="INV" + truncate_uuid,
                inventory_product=product_obj,
                inventory_stocks=product_stocks,
                inventory_created=timezone.now()
            )
            inventory_obj.save()



            messages.success(request, 'Product added successfully')
            return redirect('add_product', store_slug=store_slug)



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
        product_store = request.POST.get('product-store')

        if Product.objects.filter(product_name=product_name).exists():
            messages.error(request, 'Product already exists')
            return redirect('update_product' , store_slug=store_slug)
        else:
            category = Category.objects.get(pk=product_category)
            Product.objects.filter(pk=pk).update(
                product_name=product_name,
                product_store=store,
                product_slug=product_slug,
                product_description=product_description,
                product_category=category,
                product_price=product_price,
                product_image=product_image,
                product_created=timezone.now()
            )

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

def pos_inventory(request, store_slug):
    store = get_object_or_404(Store, store_slug=store_slug)
    inventory = Inventory.objects.filter(inventory_product__product_store=store)


    context = {
        'store': store,
        'inventories': inventory
    }
    return render(request, 'includes/pos/pos_includes/pos_inventory.html', context)

def pos_edit_inventory(request, store_slug, pk):
    store = get_object_or_404(Store, store_slug=store_slug)
    inventory = get_object_or_404(Inventory, pk=pk)

    if request.method == 'POST':
        inventory_stocks = request.POST.get('product-stocks')
        inventory_status = request.POST.get('product-status')
        Inventory.objects.filter(pk=pk).update(
            inventory_stocks=inventory_stocks,
            inventory_status=inventory_status
        )
        messages.success(request, 'Inventory updated successfully')
        return redirect('pos_inventory', store_slug=store_slug)

    context = {
        'store': store,
        'inventory': inventory
    }
    return render(request, 'includes/pos/pos_includes/edit_inventory.html', context)



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


def settings(request):
    currencies =['PHP','USD','EUR','CNY','JPY',]

    setting = Setting.objects.all()
    if setting.exists():
        for s in setting:
            settings_id = s.setting_id
        existing = True
    else:
        settings_id = 'posv100'
        existing = False

    if request.method == 'POST':
        settings_id = request.POST.get('settings_id')
        tax = request.POST.get('tax')
        currencies = request.POST.get('currencies')

        if tax == '':
            tax = 0
        if Setting.objects.filter(setting_id=settings_id).exists():
            Setting.objects.filter(setting_id=settings_id).update(
                tax=tax,
                currency=currencies
            )
        else:
            settings = Setting.objects.create(
                setting_id=settings_id,
                tax=tax,
                currency=currencies,
                setting_created=timezone.now()
            )
            settings.save()


        messages.success(request, 'Settings updated successfully')
        return redirect('settings')

    context = {
        'settings_id': settings_id,
        'currencies' : currencies,
        'existing': existing
    }
    return render(request, 'includes/settings.html', context)