import django_filters
from django_filters import CharFilter
from .models import Order, Customer, Product


class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = Order
        fields = ['status','transaction_id']


class CustomerFilter(django_filters.FilterSet):
    name = CharFilter(field_name='name',lookup_expr='icontains',label='Name')
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['email','user']


class ProductFilter(django_filters.FilterSet):
    name = CharFilter(field_name='name',lookup_expr='icontains',label='Name')
    class Meta:
        model = Product
        fields = ['name', 'category']