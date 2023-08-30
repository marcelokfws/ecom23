from django.urls import path

from . import views

urlpatterns = [
    path('search/', views.search, name='search'),
    path('add_to_carrinho/<int:product_id>/',
         views.add_to_carrinho, name='add_to_carrinho'),
    path('cart/', views.carrinho_view, name='carrinho_view'),
    path('remove/<str:product_id>/',
         views.remove_from_carrinho, name='remove_from_carrinho'),
    path('change_quantity/<str:product_id>/',
         views.change_quantity, name='change_quantity'),
    path('<slug:slug>/', views.category_details, name='category_details'),
    path('<slug:category_slug>/<slug:slug>/',
         views.products_details, name='products_details'),


]
