from products.models import Product

def contect_process(reauest):
    products=Product.objects.all()[:3]
    
    context={'product_for_all':products}
    
    return context
#def x(request):
   # p=Product.objects.all()
   # context={ 'z':p }
   # return p