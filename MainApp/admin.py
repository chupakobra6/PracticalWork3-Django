from django.contrib import admin

from MainApp import models


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    list_display_links = ['name']
    list_editable = []
    list_filter = ['name']
    search_fields = ['name', 'description']


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    list_display_links = ['name']
    list_editable = []
    list_filter = ['name']
    search_fields = ['name', 'description']


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'created_at', 'updated_at']
    list_display_links = ['name']
    list_editable = ['price']
    list_filter = ['name', 'price', 'category', 'created_at', 'updated_at']
    search_fields = ['name', 'description']


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'order_date', 'customer_name', 'customer_phone', 'delivery_address']
    list_display_links = ['order_number']
    list_filter = ['order_date', 'customer_name', 'delivery_address']
    search_fields = ['order_number']


@admin.register(models.OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'discount_per_unit']
    list_display_links = ['order']
    list_filter = ['order__order_number', 'product__name']
    search_fields = ['order__order_number', 'product__name']
