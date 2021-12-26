from django.shortcuts import render,redirect
from .models import *
from .forms import *
from .filters import OrderFilter, CustomerFilter,ProductFilter
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView,DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.core.paginator import Paginator
from .utils import cookieCart, cartData, guestOrder
from django.views.decorators.csrf import csrf_exempt
import json
import datetime
from django_xhtml2pdf.utils import pdf_decorator







def home(request):
    template_name = 'main/home.html'
    data = cartData(request)
    cardItems = data['cardItems']
    products = Product.objects.all().filter(visibilty=True).order_by('date_created')
    context ={
        "products":products,
        "cardItems":cardItems,
    }
    return render(request,template_name,context)



def cart(request):
    template_name = 'main/cart.html'
    data = cartData(request)
    cardItems = data['cardItems']
    order = data['order']
    items = data['items']


    context = {
        'items':items,
        'order':order,
        'cardItems':cardItems,
    }
    return render(request,template_name, context)

def checkout(request):
    template_name = 'main/checkout.html'
    data = cartData(request)
    cardItems = data['cardItems']
    order = data['order']
    items = data['items']
        
    context = {
        'items':items,
        'order':order,
        'cardItems':cardItems,
    }
    return render(request,template_name, context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    product = Product.objects.get(id = productId)
    order, created = Order.objects.get_or_create(complete = False,status = 'Pending')
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity) + 1
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity) - 1

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item was added', safe = False)



@csrf_exempt
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    customer, order = guestOrder(request,data)
       
    total = float(data['form']['total'])
    order.transaction_id = str(transaction_id)[11:]

    if total == order.get_cart_total:
        order.complete = True
    order.save()
    ShippingAddress.objects.create(
        name = data['form']['name'],
        phone = data['form']['number'],
        order = order,
        area = data['shipping']['area'],
        street = data['shipping']['street'],
        house_no = data['shipping']['houseno'],
    )

    return JsonResponse('Order was submitted', safe = False)





@login_required
def product(request):
    template_name = 'main/products.html'
    products = Product.objects.all()
    filter = ProductFilter(request.GET,queryset=products)
    products = filter.qs
    context ={
        "products":products,
        "filter":filter,
    }
    return render(request,template_name, context)


@login_required
def customer(request):
    template_name = 'main/customers.html'
    customers = Customer.objects.all()
    filter = CustomerFilter(request.GET, queryset=customers)
    customers = filter.qs
    context ={
        "customers":customers,
        'filter':filter,
    }
    return render(request,template_name, context)

@login_required
def orders(request):
    template_name = 'main/orders.html'
    orders = Order.objects.filter(complete = True).order_by('-date_created')
    filter = OrderFilter(request.GET, queryset=orders)
    orders = filter.qs
    paginator = Paginator(orders,20)
    page_number = request.GET.get('page')
    orders_page = paginator.get_page(page_number)
    context = {
        'filter':filter,
        "orders_page":orders_page,
    }
    return render(request,template_name,context)

@login_required
def customerOrders(request,pk):
    template_name = 'main/customer_orders.html'
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    total_orders = orders.count()
    pending = orders.filter(status = "Pending").count()
    delivered = orders.filter(status = "Delivered").count()
    ofd = orders.filter(status='Out For Delivery').count()
    context = {
        'total_orders':total_orders,
        'pending':pending,
        'delivered':delivered,
        'ofd':ofd,
        'orders':orders,
        'customer':customer
    }
    return render(request,template_name,context)


class ProductCreate(CreateView,LoginRequiredMixin):
    template_name = 'main/product_create.html'
    model = Product
    fields = '__all__'
    success_url = reverse_lazy('main:products')   


@login_required
def updateProduct(request,pk):
    product = Product.objects.get(id=pk)
    form = ProductUpdateForm(instance=product)
    if request.method == 'POST':
        form = ProductUpdateForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('main:products')
    context = {'form':form }
    return render(request, 'main/product_update.html', context)



class ProductDelete(DeleteView,LoginRequiredMixin):
    model = Product





@login_required
def dashboard(request):
    template_name = 'main/dashboard.html'
    orders = Order.objects.all().order_by('-date_created').filter(status = 'Pending')[:10]
    orders_all = Order.objects.all()
    products = Product.objects.all().order_by('date_created')
    total_orders = orders_all.count()
    ofd = orders_all.filter(status='Out For Delivery').count()
    delivered = orders_all.filter(status='Delivered').count()
    pending = orders_all.filter(status='Pending').count()
    customers = Customer.objects.all()

    context = {
        "customers":customers,
        "orders":orders,
        "total_orders":total_orders,
        "delivered":delivered,
        "ofd":ofd,
        "pending":pending,
        "products":products,
    }
    return render(request,template_name,context)


@login_required 
@csrf_exempt
def orderDetail(request,pk):
    template_name = 'main/order_detail.html'
    order = Order.objects.get(id=pk)
    items = order.orderitem_set.all()
    addresses = order.shippingaddress_set.all()
    form = OrderUpdateForm(instance=order)
    if request.method == 'POST':
        form = OrderUpdateForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
    context = {
        "addresses":addresses,
        "order":order,
        "items":items,
        "form":form,
        
    }
    return render(request,template_name,context)




def done(request):
    data = cartData(request)
    cardItems = data['cardItems']
    template_name = 'main/done.html'
    order = Order.objects.first()
    id = order.id
    order = Order.objects.get(id=id)
    items = order.orderitem_set.all()
    context = {"order":order,"items":items,"cardItems":cardItems}
    return render(request,template_name,context) 


@pdf_decorator(pdfname='SabjiWaalaBill.pdf')
def bilPDF(request,pk):
    template_name = 'main/bill_pdf.html'
    order = Order.objects.get(id=pk)
    items = order.orderitem_set.all()
    context = {"order":order,"items":items}
    return render(request,template_name,context)


def about(request):
    data = cartData(request)
    cardItems = data['cardItems']
    template_name = 'main/about_us.html'
    return render(request,template_name,context={'cardItems':cardItems})

def contact(request):
    data = cartData(request)
    cardItems = data['cardItems']
    template_name = 'main/contact_us.html'
    return render(request,template_name,context={'cardItems':cardItems})