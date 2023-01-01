from store.models import Store, Category, Product, Order, OrderItem, Transaction, Settings, Inventory

store = Store.objects.get(store_slug='mamgic-foodhub')
order = Order.objects.filter(order_store=store, order_completed=False)
order_item = OrderItem.objects.filter(order_item_order__in=order)

print(order_item)
