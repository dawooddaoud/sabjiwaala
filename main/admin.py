from django.contrib import admin
from .models import Tag, Product,Customer,ShippingAddress,Order,OrderItem
# Register your models here.
admin.site.register(Tag)
admin.site.register(Customer)
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Product)