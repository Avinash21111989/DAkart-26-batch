from django.shortcuts import render,HttpResponse
from store.models import Product

def home(request):
    Products = Product.objects.all()
    context = {
        'Products':Products
    }
    return render(request,'home.html', context)