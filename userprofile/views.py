from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.utils.text import slugify

from store.forms import ProductForm
from store.models import Product

from .models import Userprofile


def vendor_details(request, pk):
    user = User.objects.get(pk=pk)
    products = user.products.filter(status=Product.ATIVAR)
    return render(
        request, 'userprofile/vendor_details.html', {
            'user': user, 'products': products})


@login_required
def my_store(request):
    products = request.user.products.exclude(status=Product.DELETADO)
    return render(request, 'userprofile/my_store.html', {'products': products})


@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            title = request.POST.get('title')
            product = form.save(commit=False)
            product.user = request.user
            product.slug = slugify(title)
            product.save()
            messages.success(request, 'Produto cadastrado com sucesso.')
            return redirect('my_store')
    else:

        form = ProductForm()
    return render(
        request, 'userprofile/product_form.html', {
            'title': 'Adicionar Produto', 'form': form})


@login_required
def edit_product(request, pk):
    product = Product.objects.filter(user=request.user).get(pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto editado com sucesso.')
            return redirect('my_store')
    else:
        form = ProductForm(instance=product)
    return render(
        request, 'userprofile/product_form.html', {
            'title': 'Editar Produto',
            'product': product,
            'form': form})


@login_required
def minha_conta(request):

    return render(
        request, 'userprofile/minhaconta.html')


@login_required
def delete_product(request, pk):
    product = Product.objects.filter(user=request.user).get(pk=pk)
    product.status = Product.DELETADO
    product.save()
    messages.success(request, 'Produto apagado com sucesso.')
    return redirect('my_store')


def cadastrar(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            login(request, user)
            userprofile = Userprofile.objects.create(user=user)

            return redirect('home')

    else:
        form = UserCreationForm()

    return render(request, 'userprofile/cadastrar.html', {'form': form})
