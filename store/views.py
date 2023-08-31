import json

import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .carrinho import Carrinho
from .forms import OrderForm
from .models import Category, Order, OrderItem, Product


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


@login_required
def checar_comprar(request):
    carrinho = Carrinho(request)
    if request.method == 'POST':
        data = json.loads(request.body)
        form = OrderForm(request.POST)

        total_price = 0
        items = []
        for item in carrinho:
            product = item['product']
            total_price += product.price * int(item['quantity'])
            items.append({
                'price_data': {
                    'currency': 'usd',
                    'product_data': {

                        'name': product.title,
                    },
                    'unit_amount': product.price
                },
                'quantity': item['quantity']
            })

            stripe.api_key = settings.STRIPE_SECRET_KEY
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=items,
                mode='payment',
                success_url='http://127.0.0.1:8000/carrinho/success',
                cancel_url='http://127.0.0.1:8000/carrinho/',
            )

            payment_intent = session.payment_intent

            order = Order.objects.create(
                p_name=data['p_name'],
                s_name=data['s_name'],
                adress=data['adress'],
                zip_numero=data['zip_numero'],
                city=data['city'],
                criado_por=request.user,
                esta_pago=True,
                payment_intent=payment_intent,
                valor_pago=total_price
            )

            for item in carrinho:
                product = item['product']
                quantity = int(item['quantity'])
                price = product.price * quantity

                item = OrderItem.objects.create(
                    order=order, product=product,
                    price=price, quantity=quantity)
                carrinho.clear()
                return JsonResponse({
                    'session': session, 'order': payment_intent})
    else:
        form = OrderForm()
    return render(request, 'store/checar_comprar.html', {
        'carrinho': carrinho, 'form': form, 'pub_key': settings.STRIPE_PUB_KEY})  # noqa


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
