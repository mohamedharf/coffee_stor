from django.shortcuts import render ,redirect 
from django.contrib import messages 
from products.models import Product
from orders.models import Order
from . models import OrderDetails
from django.utils import timezone
from datetime import datetime
from.models import Payment

# Create your views here.
def add_to_cart (request):
    
    if 'pro_id' in request.GET and 'qty' in request.GET and 'price' in request.GET and request.user.is_authenticated and not request.user.is_anonymous:
        pro_id= request.GET['pro_id']
        qty = request.GET['qty']
        order = Order.objects.all().filter(user=request.user , is_finished=False)
       
        if not Product.objects.all().filter(id=pro_id).exists():
           return redirect('products')
       
        pro =Product.objects.get(id=pro_id)
       
        if order:
            old_order=Order.objects.get(user=request.user , is_finished=False )
            orderdetails=OrderDetails.objects.create(product=pro , order=old_order , price=pro.price ,quantity=qty)
            
            
            messages.success(request , 'old + new order')

        else:
            new_order = Order()
            new_order.user = request.user
            new_order.order_date=timezone.now() 
            #اعرفلي كسم الغلط فين 
            #new_order.order_date=timezone() 
            new_order.is_finished=False
            new_order.save()
            orderdetails =OrderDetails.objects.create( product=pro , order=new_order ,price=pro.price ,quantity=qty )
            messages.success(request , 'new order')

        return redirect('/products/' + request.GET['pro_id']) 
    else:
        if 'pro_id' in request.GET:
            
         messages.error(request , 'pleas logn in')
         return redirect('/products/' + request.GET['pro_id']) 
        else:

         return redirect ('index' )


def cart(request):
    context= None
    if request.user.is_authenticated and not request.user.is_anonymous:
        if Order.objects.all().filter(user=request.user , is_finished=False):
            order=Order.objects.get(user=request.user ,is_finished=False)
            orderdetails = OrderDetails.objects.all().filter(order=order)
            total=0
            for sub in orderdetails:
                total += sub.price * sub.quantity
            context={
                'order':order,
                'orderdetails':orderdetails,
                'total':total,
                
            }
    return render(request, 'orders/cart.html' , context)

def remove_from_cart(request , orderdetails_id):
    if request.user.is_authenticated and  not request.user.is_anonymous and orderdetails_id:
        
        orderdetails =OrderDetails.objects.get(id=orderdetails_id)
        if orderdetails.order.user.id==request.user.id:
        
          orderdetails.delete()
    return redirect('cart')


def add_qty(request , orderdetails_id):
    if request.user.is_authenticated and  not request.user.is_anonymous and orderdetails_id:
        orderdetails =OrderDetails.objects.get(id=orderdetails_id)
        
        if orderdetails.order.user.id==request.user.id:

         orderdetails.quantity +=1
         orderdetails.save()
    return redirect('cart')


def sub_qty(request , orderdetails_id):
    if request.user.is_authenticated and  not request.user.is_anonymous and orderdetails_id:
        orderdetails =OrderDetails.objects.get(id=orderdetails_id)
        if orderdetails.order.user.id==request.user.id:
       
         if   orderdetails.quantity>1: orderdetails.quantity -=1
        orderdetails.save()
    return redirect('cart')


def payment(request):
    context=None
    ship_address=None
    ship_phone=None
    card_number=None
    expire=None
    security_code =None
    is_added=None
   
    
    if request.method=='POST' and 'btnpymint' in request.POST:
         ship_address=request.POST['shipment_address']
         ship_phone=request.POST['ship_phone']
         card_number=request.POST['card_number']
         expire=request.POST['expire']
         security_code =request.POST['security_code']
         if request.user.is_authenticated and not request.user.is_anonymous:
            if Order.objects.all().filter(user=request.user , is_finished=False):
             order=Order.objects.get(user=request.user ,is_finished=False)
            
            payment = Payment(order=order , shipment_address=ship_address ,shipment_phone=ship_phone , card_number=card_number , expire=expire ,security_code=security_code )
            payment.save()
            order.is_finished=True
            order.save()
            is_added=True
            messages.success(request, ' ordeer is finish')
    
         context={
            'ship_address': ship_address,
            'ship_phone':ship_phone,
            'card_number':card_number,
            'expire':expire,
            'security_code':security_code,
            'is_added':is_added,
            
        }
    else:
        #العرض قبل الدفع 
        if request.user.is_authenticated and not request.user.is_anonymous:
            if Order.objects.all().filter(user=request.user , is_finished=False):
                order=Order.objects.get(user=request.user ,is_finished=False)
                orderdetails = OrderDetails.objects.all().filter(order=order)
                total=0
                for sub in orderdetails:
                    total += sub.price * sub.quantity
                context={
                    'order':order,
                    'orderdetails':orderdetails,
                    'total':total,
                    
                }
    return render(request , 'orders/payment.html' , context)
def show_orders(request):
    context=None
    all_orders=None
    if request.user.is_authenticated and not request.user.is_anonymous:
        all_orders= Order.objects.all().filter(user=request.user )
        if Order.objects.all().filter(user=request.user , is_finished=False):
           order=Order.objects.get(user=request.user ,is_finished=False)
           orderdetails = OrderDetails.objects.all().filter(order=order)
           total=0
           for sub in orderdetails:
                total += sub.price * sub.quantity
    context={'all_orders':all_orders} 
    return render(request , 'orders/SHOW_ORDER.html' , context)