from django.shortcuts import render, get_object_or_404
from store.models import Product
from category.models import category
from django.db.models import Q

# Create your views here.
def store(request,category_url=None):
    if category_url !=None:
        categories = get_object_or_404(category,slug=category_url)
        Products = Product.objects.filter(category=categories,is_available=True)
        product_count = Products.count()
    else:
        Products = Product.objects.all()
        product_count = Products.count()

    context = {
        'Products':Products,
        'product_count':product_count
    }

    return render(request,'store.html',context)
def product_detail(request,category_url,product_url):
    try:
        single_product = Product.objects.get(category__slug=category_url,slug=product_url)
    except:
        pass
    context = {
        'single_product':single_product
    }
    return render(request,'product_detail.html',context)

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        Products=Product.objects.filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
        product_count = Products.count()

        context = {
            'Products':Products,
            'product_count':product_count
        }

    return render(request,'store.html',context)