from django.db import models
from django.contrib.auth.models import User



# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User,blank=True,null=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True,blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name





class Tag(models.Model):
    name = models.CharField(max_length=200,null = True)

    def __str__(self):
        return self.name




class Product(models.Model):
    CATEGORY = (
        ("Fruit","Fruit"),
        ("Vegetable","Vegetable"),
    )
    name = models.CharField(max_length=200, null=True)
    market_price = models.FloatField(null=True)
    shop_price = models.FloatField(null=True)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    pic = models.ImageField(default = 'default.png', null=True,blank=True)
    tag = models.ManyToManyField(Tag,blank=True)
    visibilty = models.BooleanField(default=True,blank=True,null=True)
    class Meta:
        ordering = ['date_created']

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS = (
        ("Pending","Pending"),
        ("Out For Delivery","Out For Delivery"),
        ("Delivered","Delivered"),
    )
    customer =  models.ForeignKey(Customer,blank=True, null=True, on_delete= models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False,null=True,blank=True)
    status = models.CharField(max_length=20,choices=STATUS,null=True)
    transaction_id = models.CharField(max_length=200,null=True)
    

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total  = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        count = 0
        for item in orderitems:
            count = count + 1
        return count
        




class OrderItem(models.Model):
    product =  models.ForeignKey(Product,blank=True, null=True, on_delete= models.SET_NULL)
    order =  models.ForeignKey(Order,blank=True, null=True, on_delete= models.SET_NULL)
    quantity = models.IntegerField(default= 0 ,null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)


    @property
    def get_total(self):
        total = self.product.shop_price * self.quantity
        return total


class ShippingAddress(models.Model):
    name =  models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    order =  models.ForeignKey(Order,blank=True, null=True, on_delete= models.SET_NULL)
    area =  models.CharField(max_length=200,null=True, blank= True)
    street = models.CharField(max_length=200,null=True, blank= True)
    house_no = models.CharField(max_length=200,null=True, blank= True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.street