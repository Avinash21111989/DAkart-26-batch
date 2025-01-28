from django.shortcuts import render,redirect,get_object_or_404
from . models import Cart,CartItem
from store.models import Product
# Create your views here.
def cart_id(request):
    cartId = request.session.session_key
    if not cartId:
        cartId = request.session.create()
    return  cartId

def add_cart(request,product_id):
    my_product = Product.objects.get(id=product_id)
    print("product is",my_product)
    try:
       
       new_cart=  Cart.objects.get(cart_id=cart_id(request))
       print("the code is in try block")
    except Cart.DoesNotExist:
        new_cart = Cart.objects.create(cart_id = cart_id(request))
        print("the code is in except blovk")
    
    if request.user.is_authenticated:
        cart_item_exists = CartItem.objects.filter(product = my_product,user=request.user).exists()
        if cart_item_exists:
            cart_items = CartItem.objects.filter(product = my_product,user=request.user)
            for item in cart_items:
                item.quantity +=1
                item.save()
        else:
            item = CartItem.objects.create(product = my_product, quantity =1, user = request.user)

    cart_item_exists = CartItem.objects.filter(product = my_product,cart=new_cart).exists()
    print("cart item exists", cart_item_exists)
    if cart_item_exists:
        cart_items = CartItem.objects.filter(product = my_product,cart=new_cart)
        for item in cart_items:
            item.quantity +=1
            item.save()
    else:
        CartItem.objects.create(product= my_product , quantity = 1, cart = new_cart)


    return redirect('cart')

def cart(request,total = 0, tax =0,grand_total=0,cart_items = None):
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user,is_active=True)
        else:
            custom_cart_id = Cart.objects.get(cart_id = cart_id(request))
            cart_items = CartItem.objects.filter(cart=custom_cart_id,is_active=True)

    except:
       pass

    if cart_items!= None:
        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity

    
        tax = (2 * total)/100
        grand_total = total + tax

    context = {
            'total':total,
            'cart_items':cart_items,
            'tax':tax,
            'grand_total':grand_total

    }


    return render(request,'cart.html',context)

def remove_cartItem(request, product_id):
    product_id = get_object_or_404(Product, id = product_id)
    
    try:
        custom_cart = Cart.objects.get(cart_id = cart_id(request))
        cart_Items = CartItem.objects.get(product = product_id,cart = custom_cart)
    except:
        pass
    
    if cart_Items.quantity > 1:
        cart_Items.quantity -= 1
        cart_Items.save()
    else:
        cart_Items.delete()
    
    return redirect('cart')

def checkout(request,total = 0, tax =0,grand_total=0,cart_items = None):
    try:
        custom_cart_id = Cart.objects.get(cart_id = cart_id(request))
        cart_items = CartItem.objects.filter(cart=custom_cart_id)
    except:
       pass

    if cart_items!= None:
        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity

    
        tax = (2 * total)/100
        grand_total = total + tax
    
    context = {
            'total':total,
            'cart_items':cart_items,
            'tax':tax,
            'grand_total':grand_total

    }

    return render(request,'checkout.html',context)    






   

   
