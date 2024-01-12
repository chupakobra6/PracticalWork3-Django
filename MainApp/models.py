import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    image = models.ImageField(upload_to='media/product_images/', verbose_name='Картинка')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    is_deleted = models.BooleanField(default=False, verbose_name='Логическое удаление')

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='Категория')
    tags = models.ManyToManyField(Tag, related_name='products', verbose_name='Теги')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['name']

    def __str__(self):
        return self.name


class Order(models.Model):
    order_number = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,
                                    verbose_name='Уникальный номер')
    order_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    delivery_address = models.TextField(verbose_name='Адрес доставки')
    customer_phone = models.CharField(max_length=15, verbose_name='Телефон клиента')
    customer_name = models.CharField(max_length=255, verbose_name='ФИО клиента')
    products = models.ManyToManyField(Product, through='OrderItem', verbose_name='Товары')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['order_date']

    def __str__(self):
        return str(self.order_number)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveIntegerField(verbose_name='Количество товаров на позиции')
    discount_per_unit = models.DecimalField(max_digits=5, decimal_places=2, default=0,
                                            verbose_name='Скидка за единицу товара')

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказа'
        ordering = ['order__order_number']

    def __str__(self):
        return str(self.order.order_number)
