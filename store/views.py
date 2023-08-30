from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .carrinho import Carrinho
from .models import Category, Product


def add_to_carrinho(request, product_id):
    carrinho = Carrinho(request)
    carrinho.add(product_id)

    return redirect('carrinho_view')


def change_quantity(request, product_id):
    action = request.GET.get('action', '')
    if action:
        quantity = 1
        if action == 'decrease':
            quantity = -1
        carrinho = Carrinho(request)
        carrinho.add(product_id, quantity, True)
    return redirect('carrinho_view')


def remove_from_carrinho(request, product_id):
    carrinho = Carrinho(request)
    carrinho.remove(product_id)

    return redirect('carrinho_view')


def carrinho_view(request):
    carrinho = Carrinho(request)

    return render(request, 'store/carrinho_view.html', {'carrinho': carrinho})


def category_details(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.filter(status=Product.ATIVAR)
    return render(request, 'store/category_details.html', {'category': category, 'products': products})  # noqa


def products_details(request, category_slug, slug):
    product = get_object_or_404(Product, slug=slug, status=Product.ATIVAR)
    return render(request, 'store/products_details.html', {'product': product})


def search(request):
    query = request.GET.get('query', '')
    products = Product.objects.filter(status=Product.ATIVAR).filter(
        Q(title__icontains=query) | Q(description__icontains=query))
    return render(
        request, 'store/search.html', {'query': query, 'products': products})
