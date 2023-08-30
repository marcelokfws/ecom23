from io import BytesIO

from django.contrib.auth.models import User
from django.core.files import File
from django.db import models
from PIL import Image


class Category(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title


class Product(models.Model):

    RASCUNHO = 'rascunho'
    ESPERAR_APROVACAO = 'esperando aprovacao'
    ATIVAR = 'ativado'
    DELETADO = 'deletado'

    ESTATUS_ESCOLHA = (
        (RASCUNHO, 'Rascunho'),
        (ESPERAR_APROVACAO, 'Esperando aprovação'),
        (ATIVAR, 'Ativado'),
        (DELETADO, 'Deletado')
    )
    user = models.ForeignKey(
        User, related_name="products", on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category, related_name="products", on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    description = models.TextField(blank=True)
    price = models.FloatField()
    image = models.ImageField(
        upload_to='uploads/products_images/', blank=True, null=True)
    thumbnail = models.ImageField(
        upload_to='uploads/products_images/thumbnail/',
        blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=50, choices=ESTATUS_ESCOLHA, default=ATIVAR)

    class Meta:
        ordering = ('created_at', )

    def __str__(self):
        return self.title

    def get_display_price(self):
        return (f'R${self.price:.2f}').replace('.', ',')

    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.create_thumbnail(self.image)
                self.save()
                return self.thumbnail.url
            else:
                return 'https://via.placeholder.com/240x240.jpg'

    def create_thumbnail(self, image, size=(300, 300)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)
        name = image.name.replace('uploads/products_images/', '')
        thumbnail = File(thumb_io, name=name)
        return thumbnail
