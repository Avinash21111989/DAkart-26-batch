from . models import Cart,CartItem
from . views import cart_id
def cartCounter(request,custom_cart=None):
    cart_count = 0
    try:
        custom_cart = Cart.objects.get(cart_id = cart_id(request))
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user,is_active=True)
            cart_count = cart_items.count()
        else:
            cart_items = CartItem.objects.all().filter(cart=custom_cart)
        
            cart_count = cart_items.count()
    except:
        cart_count=0

    return dict(count = cart_count)