from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [

    path('vendors/<int:pk>/', views.vendor_details, name='vendor_details'),
    path('cadastrar/', views.cadastrar, name='cadastrar'),
    path('login/', auth_views.LoginView.as_view(
        template_name='userprofile/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        template_name='userprofile/logout.html'), name='logout'),
    path('minhaconta/', views.minha_conta, name='minhaconta'),
    path('my_store/', views.my_store, name='my_store'),
    path('store/add_product/', views.add_product, name='add_product'),
    path('store/edit_product/<int:pk>/',
         views.edit_product, name='edit_product'),
    path('store/pedido/<int:pk>/',
         views.my_store_pedido_detalhe,
         name='my_store_pedido_detalhe'),
    path('store/delete_product/<int:pk>/',
         views.delete_product, name='delete_product'),

]
