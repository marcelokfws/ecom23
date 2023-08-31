from django import forms

from .models import Order, Product


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ()  # ('p_name', 's_name', 'adress', 'zip_number', 'city',)
        # 'valor_custo', 'esta_pago', 'payment_intent', 'criado_por',
        # 'created_at')


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('category', 'title', 'description', 'price', 'image')
        widgets = {
            'category': forms.Select(attrs={
                'class': 'w-full p-1 border border-gray-500'
            }),
            'title': forms.TextInput(attrs={
                'class': 'w-full p-1 border border-gray-500'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full p-1 border border-gray-500'
            }),
            'price': forms.TextInput(attrs={
                'class': 'w-full p-1 border border-gray-500'
            }),
            'image': forms.FileInput(attrs={
                'class': 'w-full p-1 border border-gray-500'
            }),
        }
