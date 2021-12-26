import json
from .models import *


def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    items = []
    order = {
        'get_cart_total':0,
        'get_cart_items':0,
    }
    cardItems = order['get_cart_items']

    count = 0
    for i in cart:
        try:
            count += 1
            cardItems = count
            product = Product.objects.get(id=i)
            total = (product.shop_price * cart[i]['quantity'])
            order['get_cart_total'] += total
            order['get_cart_items'] += count

            item = {
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'market_price': product.market_price,
                    'shop_price': product.shop_price,
                    'category': product.category,
                    'pic': product.pic,
                    },
                'quantity':cart[i]['quantity'],
                'get_total':total,
                }
            items.append(item)
        except:
            pass
    return {'cardItems':cardItems,'order':order, 'items':items}


def cartData(request):
    cookieData = cookieCart(request)
    cardItems = cookieData['cardItems']
    order = cookieData['order']
    items = cookieData['items']

    return {'cardItems':cardItems,'order':order, 'items':items}


def guestOrder(request,data):
    name = data['form']['name']
    phone = data['form']['number']

    cookieData = cookieCart(request)
    items = cookieData['items']
    customer ,created = Customer.objects.get_or_create(phone = phone)
    customer.name = name
    customer.save()
    order = Order.objects.create(customer= customer,complete=False,status = 'Pending')

    for item in items:
        id = item['product']['id']
        product = Product.objects.get(id=id)
        orderItem = OrderItem.objects.create(
            product = product,
            order = order,
            quantity = item['quantity']
        )
    return customer, order