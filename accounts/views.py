from django.shortcuts import render, redirect
from . forms import RegistrationForm,UserForm, UserProfileForm
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from . models import UserProfile
from django.contrib.auth.decorators import login_required
from carts.models import Cart,CartItem
from carts.views import cart_id

# Create your views here.
def register(request):
    if request.method == 'POST':
        print(request.POST)
        form = RegistrationForm(request.POST)
        
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            user_email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user_username = user_email.split("@")[0]

            user_isexists = User.objects.filter(username = user_username).exists()
            if user_isexists == False:
               
               user =  User.objects.create_user(
                   username = user_username,
                   first_name = first_name,
                   last_name = last_name,
                   email = user_email,
                   password = password,
                   is_active = False

                )
               
               user.save()
               profile = UserProfile()
               profile.user_id = user.id
               profile.save()

               mail_subject = "Please activate your account"
               current_site = get_current_site(request)
               email_from = settings.EMAIL_HOST_USER
               message = render_to_string('Accounts/account_verification_email.html',{
                   'user':user,
                   'domain':current_site,
                   'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                   'token':default_token_generator.make_token(user)
               })
               to_email = [user_email,]

               send_mail(mail_subject,message,email_from,to_email)
               return redirect('/accounts/login?command=verification&email='+user_email)
            else:
                messages.warning(request,"User already exists ")
                return render(request,'Accounts/register.html') 

        else:
            print(form.errors,"there are some errors")
            errors = form.errors
            messages.warning(request,errors)
            context = {
                'errors':form.errors
            }
            return render(request,'Accounts/register.html',context)

    form = RegistrationForm()
    context = {
        'form':form
    }
    
    return render(request,'Accounts/register.html',context)

def user_login(request):
    print("login details", request.POST)
    if request.method == 'POST':
        entered_username = request.POST['username']
        enetred_password  = request.POST['password']

        loggedin_user = auth.authenticate(username = entered_username, password = enetred_password)
        if loggedin_user is not None:
            try:
                cart_item = Cart.objects.get(cart_id = cart_id(request))
                print("hello inisde try")
                is_cart_item_exists = CartItem.objects.filter(cart=cart_item).exists()

            except:
                print("except block")
                print(cart_id(request))
                pass

            if is_cart_item_exists:
                cart_item = CartItem.objects.filter(cart=cart_item,is_active=True)
                for item in cart_item:
                    item.user = loggedin_user
                    item.save()

            auth.login(request,loggedin_user)

            print("login user details",loggedin_user.username)
            return redirect('home')
        else:
            user_isactive = User.objects.filter(username = entered_username,is_active = True)
            if user_isactive.exists() == False:
                messages.warning(request, "Your account is not activated, Please activate your account")
            else:
                messages.warning(request,"Invalid credentials")
        return redirect('login')

        
        



    return render(request,'Accounts/login.html')

def logout(request):
    auth.logout(request)
    messages.success(request,'You have logged out')
    return redirect('login')

def activate(request,uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk = uid)
        except(User.DoesNotExist):
            user = None
        
        if User is not None and default_token_generator.check_token(user,token):
            user.is_active = True
            user.save()
            return redirect('login')
        else:
            return redirect('registration')
        
@login_required(login_url= 'login')
def dashboard(request):
    return render(request,'accounts/dashboard.html')

@login_required(login_url= 'login')        
def editProfile(request):
    user_profile = None
    try:
        user_profile = UserProfile.objects.get(user_id = request.user.id)
    except:
        pass

    if request.method == 'POST':
        print("data", request.FILES)
        user_form = UserForm(request.POST, instance=request.user)
        user_profile_form = UserProfileForm(request.POST,request.FILES, instance = user_profile)
        if user_form.is_valid() and user_profile_form.is_valid():
            user_form.save()
            user_profile_form.save()
            messages.success(request,"Your profile is updated")
            return redirect("editProfile")
        else:
            print("error",user_form.errors)
    else:
        print("Im in else block ")
        user_form = UserForm(instance = request.user)
        user_profile_form = UserProfileForm(instance = user_profile)
    context = {
        'user_form':user_form,
        'user_profile_form':user_profile_form,
        'user_profile':user_profile
    }

    print("context dATA", context)

		
    return render(request,'accounts/edit_profile.html',context)

@login_required(login_url= 'login')
def changePassword(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_new_password = request.POST['confirm_new_password']

        user = User.objects.get(username__iexact= request.user.username)

        if new_password == confirm_new_password:
           checkPassword =  user.check_password(current_password)
           if checkPassword:
               user.set_password(new_password)
               user.save()
               messages.success(request,"Your password updated. Please login with updated password.")
               auth.logout(request)
               return redirect('changePassword')
           else:
               messages.warning(request,"Please eneter correct current password")
        else:
            messages.warning(request,"New password and confirm password not matching")
    return render(request,'accounts/change_password.html')

def myOrders(request):
    return render(request,'accounts/edit_profile.html')
