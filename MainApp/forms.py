from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, TextInput, Textarea, NumberInput, ClearableFileInput, CheckboxInput, SelectMultiple, \
    EmailField, EmailInput, PasswordInput, Form, CharField
from django.forms import Select

from MainApp.models import Category, Tag, Product, Order, OrderItem


class RegisterForm(UserCreationForm):
    email = EmailField(widget=EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'password1': PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'password2': PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        }


class LoginForm(Form):
    username = CharField(widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = CharField(widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': 'form-control'}),
        }


class TagForm(ModelForm):
    class Meta:
        model = Tag
        fields = ['name', 'description']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': 'form-control'}),
        }


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'is_deleted', 'category', 'tags']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': 'form-control'}),
            'price': NumberInput(attrs={'class': 'form-control'}),
            'image': ClearableFileInput(attrs={'class': 'form-control'}),
            'is_deleted': CheckboxInput(attrs={'class': 'form-check-input'}),
            'category': Select(attrs={'class': 'form-control'}),
            'tags': SelectMultiple(attrs={'class': 'form-control'}),
        }


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['delivery_address', 'customer_phone', 'customer_name']
        widgets = {
            'delivery_address': Textarea(attrs={'class': 'form-control'}),
            'customer_phone': TextInput(attrs={'class': 'form-control'}),
            'customer_name': TextInput(attrs={'class': 'form-control'}),
        }


class OrderItemForm(ModelForm):
    class Meta:
        model = OrderItem
        fields = ['order', 'product', 'quantity', 'discount_per_unit']
        widgets = {
            'order': Select(attrs={'class': 'form-control'}),
            'product': Select(attrs={'class': 'form-control'}),
            'quantity': NumberInput(attrs={'class': 'form-control'}),
            'discount_per_unit': NumberInput(attrs={'class': 'form-control'}),
        }
