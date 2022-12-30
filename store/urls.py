from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('settings/', views.settings, name='settings'),
    path('store-list/', views.store_list, name='store_list'),
    path('store-list/add/', views.add_store, name='add_store'),
    path('store-list/delete/<int:id>', views.delete_store, name='delete_store'),
    path('store-list/edit/<int:id>', views.edit_store, name='edit_store'),
    # POS URLS
    path('<slug:store_slug>/', views.pos_dashboard, name='pos_dashboard'),
    #POS Categories
    path('<slug:store_slug>/categories/', views.pos_categories, name='pos_categories'),
    path('<slug:store_slug>/categories/add/', views.add_category, name='add_category'),
    path('<slug:store_slug>/categories/update/<int:pk>', views.update_category, name='update_category'),
    path('<slug:store_slug>/categories/delete/<int:pk>', views.delete_category, name='delete_category'),
    #POS
    path('<slug:store_slug>/point-of-sales/', views.pos, name='pos'),
    path('<slug:store_slug>/point-of-sales/add-order/<int:pk>', views.add_order, name='add_order'),
    path('<slug:store_slug>/point-of-sales/update-order/<int:pk>', views.update_order, name='update_order'),
    path('<slug:store_slug>/point-of-sales/delete-order/<int:pk>', views.delete_order, name='delete_order'),
    path('<slug:store_slug>/point-of-sales/orders/', views.pos_orders, name='pos_orders'),
    path('<slug:store_slug>/point-of-sales/orders/getOrder/', views.pos_getOrders, name='pos_getOrders'),
    #POS Sales
    path('<slug:store_slug>/sales/', views.pos_sales, name='pos_sales'),
    path('<slug:store_slug>/sales/receipts/<int:pk>', views.pos_getReceipt, name='pos_getReceipt'),
    path('<slug:store_slug>/sales/receipts/delete/<int:pk>', views.pos_deleteReceipt, name='pos_deleteReceipt'),
    #POS Products
    path('<slug:store_slug>/products/', views.pos_products, name='pos_products'),
    path('<slug:store_slug>/products/add/', views.add_product, name='add_product'),
    path('<slug:store_slug>/products/update/<int:pk>', views.update_product, name='update_product'),
    path('<slug:store_slug>/products/delete/<int:pk>', views.delete_product, name='delete_product'),
    #Coming Soon
    path('<slug:store_slug>/customers/', views.pos_customers, name='pos_customers'),
    path('<slug:store_slug>/messages/', views.pos_messages, name='pos_messages'),
    
]