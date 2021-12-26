from django.forms import  ModelForm
from .models import Tag, Product, Order



class ProductUpdateForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['pic','categoty','tag']


class OrderUpdateForm(ModelForm):
    class Meta:
        model = Order
        fields = ['status']