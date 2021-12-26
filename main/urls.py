from django.urls import path
from . import views
from django.urls import reverse_lazy

app_name = 'main'
urlpatterns = [
    path('',views.home,name='main'),
    path('cart/', views.cart, name = 'cart'),
    path('checkout/', views.checkout, name = 'checkout'),
    path('products/', views.product, name = "products" ),
    path('update_item/', views.updateItem, name = 'update_item'),
    path('process_order/', views.processOrder, name = 'process_order'),
    path('products/update/<int:pk>', views.updateProduct, name = "product_update"),
    path('products/create/', views.ProductCreate.as_view() , name = "product_create"),
    path('products/<int:pk>/delete',views.ProductDelete.as_view(success_url=reverse_lazy('main:products')), name='product_delete'),
    path('orders/',views.orders, name = 'orders'),
    path('orders/<int:pk>',views.orderDetail,name ='order_items'),
    path('customers/',views.customer, name = 'customers'),
    path('customers/<int:pk>',views.customerOrders,name ='customer_orders'),
    path('dashboard/',views.dashboard, name = 'dashboard'),    
    path('done/',views.done,name = 'done'),
    path('pdf/<int:pk>',views.bilPDF,name = 'pdf'),
    path('about_us/',views.about,name = 'about'),
    path('contact_us/',views.contact,name = 'contact'),
]

