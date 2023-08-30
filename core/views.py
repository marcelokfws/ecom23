from django.shortcuts import render

from store.models import Product


def home(request):
    products = Product.objects.filter(status=Product.ATIVAR)[0:6]
    return render(request, 'core/home.html', {'products': products})


def sobre(request):
    return render(request, 'core/sobre.html')
