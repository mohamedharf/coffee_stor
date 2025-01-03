from django.shortcuts import render ,redirect
from django.contrib import messages
from django.contrib.auth.models import User 
from django.contrib import auth
from .models import UserProfile
import re
from django.contrib.auth.decorators import login_required
from products.models import Product


# Create your views here.
def signin(request):
    
  if request.method == 'POST' and 'btnlogin' in request.POST:
        
      username=request.POST['user']
      password=request.POST['pass']
      
      user = auth.authenticate(username=username ,password=password )
      if user is not None:
          if 'rememberme' not in request.POST:
              request.session.set_expiry(0)
              
          auth.login(request , user)
         # messages.success(request , 'you are logged in ')
      else:
          messages.error(request , 'username or password invalid')
      
      return redirect('signin')
  else:
      
   return render(request,'accounts/signin.html' )


def logout(request):
   if request.user.is_authenticated:
       auth.logout(request)
   return redirect('index')

def signup(request):
    if request.method =='POST' and 'btnsignup' in request.POST:
        
        #variables for fileds
        fname=None
        lname=None
        address=None
        address2=None
        city=None
        state=None
        zip_number=None
        email=None
        username=None
        password=None
        terms=None
        is_added=None
        
        #get values from the form    
        #fname=request.POST['fname']  
        
        if 'fname' in request.POST: fname= request.POST['fname']
        else:messages.error(request , 'eroor in frist name')
        if 'lname' in request.POST: lname= request.POST['lname']
        else:messages.error(request , 'eroor in last name')

        if 'address' in request.POST : address = request.POST['address']
        else: messages.eroor(request , 'EROOR IN ADDREES')
        if 'address2' in request.POST : address2=request.POST['address2']
        else: messages.eroor(request , 'EROOR IN ADDREES2')
        
        
        if 'city' in request.POST : city =request.POST['city']
        else: messages.error(request , 'EROOR IN CITY')
        
        if 'state' in request.POST : state=request.POST['state']
        else: messages.error(request ,'eroor in state')
        
        
        if 'zip' in request.POST : zip_number =request.POST["zip"]
        else:messages.error(request , 'eroor in ZIP')
        
        
        if 'email' in request.POST :email =request.POST['email']
        else:messages.error(request , 'eroor in E_MAIL')

        if 'user' in request.POST: username=request.POST['user']
        else:messages.error(request , 'eroor in USER_NAME')
        
        if 'pass' in request.POST : password= request.POST['pass']
        else:messages.error(request , 'eroor in PASSWORD')
        
        if 'terms' in request.POST : terms= request.POST['terms']


        # check the values
        if fname and lname and address and address2 and city and state and zip_number and email and username and password :
            signin
            #terms in check
            if terms =='on':
               #check if username is taken
               if User.objects.filter(username=username).exists():
                   messages.error(request , 'the user name is taken')
               else:
                   #check if email is taken
                   if User.objects.filter(email = email).exists():
                       messages.error(request , 'the email is taken')
                   else:
                       patt= "^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$"
                       if re.match(patt , email):
                           #add user 
                           user =User.objects.create_user(first_name=fname ,last_name=lname ,email=email ,username=username , password=password )
                           user.save()
                           #add user profile
                           userprofile = UserProfile (user = user , address=address , address2=address2 , city=city , stat=state ,zip_number=zip_number )
                           userprofile.save()
                           #clear fildes
                           fname= ''
                           lname= ''
                           address= ''
                           address2= ''
                           city= ''
                           state= ''
                           zip_number= ''
                           email= ''
                           username= ''
                           password= '' 
                           terms=None
                           #sucsess message
                           messages.success(request , 'DONE')
                           is_added =True 
                           
                       else:
                           messages.error(request , 'invalid email')
                           

            else:
                messages.error(request , 'your must agree to the terms')
            
        else:messages.error(request , 'CHECK EMPTY FIELDS')
        
              
        
        
        return render(request , 'accounts/signup.html' , {
            
           'fnamee':fname,
           'lname':lname,
           'address':address,
           'address2':address2,
           'city':city,
           'state':state,
           'zip':zip_number,
           'email':email,
           'user':username,
           'pass':password, 
           'is_added':is_added
      
        })
    
    else:
     return render(request , 'accounts/signup.html')




@login_required()
def profile(request):
    if request.method == 'POST' and 'btnsave' in request.POST:
        if request.user is not None and request.user.id !=None:
            userprofile =UserProfile.objects.get(user=request.user)
            if request.POST['fname'] and request.POST['lname'] and request.POST['address'] and request.POST['pass']:
                request.user.first_name = request.POST['fname'] 
                request.user.last_name = request.POST['lname']
              #  request.user.email =request.POST['email']
                userprofile.address =request.POST['address']
                userprofile.address2 =request.POST['address2']
                userprofile.city=request.POST['city']
                userprofile.stat =request.POST['state']
                userprofile.zip_number =request.POST['zip']
              #  request.user.username =request.POST['username']
                if not request.POST['pass'].startswith('pbkdf2_sha256$'):
                    request.user.set_password(request.POST['pass'])
               # else:
                  #  request.user.password = request.POST['pass']
                request.user.save()
                userprofile.save()
                auth.login(request , request.user)
                messages.success(request , ' done save')
            else:
                messages.error(request , 'check your values and elements ')
        return redirect('profile')
        
    else:
      #if request.user.is_anonymous:return redirect('index')
      #if request.user.id==None:return redirect('index')
      
      if request.user is not None:
          context=None
          #if not request.user.is_anonymous:
          if request.user.id !=None:
            userprofile=UserProfile.objects.get(user=request.user)

            context={
              'fname':request.user.first_name,
              'lname':request.user.last_name,
              'address':userprofile.address,
              'address2':userprofile.address2,
              'city':userprofile.city,
              'stat':userprofile.stat,
              'zip_number':userprofile.zip_number,
              'email':request.user.email,
              'user':request.user.username,
              'pass':request.user.password
              
              
            }
          return render(request , 'accounts/profile.html' , context)
      else:
          return redirect('profile')  
      
      
      
      
def product_favorite(request , pro_id):
    
   if request.user.is_authenticated and not request.user.is_anonymous :
       pro_fav = Product.objects.get(pk=pro_id)
       if UserProfile.objects.filter(user=request.user , product_favorites=pro_fav).exists():
           messages.success(request , 'product in the favorit')
       else:
           userProfile =UserProfile.objects.get(user=request.user)
           userProfile.product_favorites.add(pro_fav)
           messages.success(request , 'product has been favorit')
           
       
   else:
      messages.error(request , ' pleas sign in') 

   return redirect('/products/' + str(pro_id))




def show_favorite_product(request):
    context=None
    if request.user.is_authenticated and not request.user.is_anonymous :
        userInfo =UserProfile.objects.get(user=request.user)
        pro =userInfo.product_favorites.all()
        context= { 'products':pro }
        
    
    
    return render(request , 'products/products.html' , context)
           
