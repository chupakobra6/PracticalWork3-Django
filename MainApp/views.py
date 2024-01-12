from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from rest_framework import permissions

from MainApp.forms import ProductForm, CategoryForm, OrderForm, TagForm, RegisterForm
from MainApp.models import Product, Tag, Category, Order


@login_required(login_url='login')
def user_profile(request):
    return render(request, 'user_profile.html')


class RegisterView(View):
    template_name = 'register.html'
    form_class = RegisterForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        return render(request, self.template_name, {'form': form})


def home(request):
    return render(request, 'home.html')


def paginate_objects(request, objects, per_page):
    paginator = Paginator(objects, per_page)
    page = request.GET.get('page')

    try:
        paginated_objects = paginator.page(page)
    except PageNotAnInteger:
        paginated_objects = paginator.page(1)
    except EmptyPage:
        paginated_objects = paginator.page(paginator.num_pages)

    return paginated_objects


class CategoryListView(ListView):
    model = Category
    template_name = 'catalog/categories_list.html'
    context_object_name = 'categories'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['paginated_objects'] = paginate_objects(self.request, context['categories'], self.paginate_by)
        return context


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'catalog/category_detail.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.filter(category=self.object)
        return context


class CategoryCreateView(CreateView):
    model = Category
    template_name = 'catalog/category_form.html'
    form_class = CategoryForm
    success_url = reverse_lazy('product_list')

    @method_decorator(login_required(login_url='login'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class TagListView(ListView):
    model = Tag
    template_name = 'catalog/tags_list.html'
    context_object_name = 'tags'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['paginated_objects'] = paginate_objects(self.request, context['tags'], self.paginate_by)
        return context


class TagDetailView(DetailView):
    model = Tag
    template_name = 'catalog/tag_detail.html'
    context_object_name = 'tag'


class TagCreateView(CreateView):
    model = Tag
    template_name = 'catalog/tag_form.html'
    form_class = TagForm
    success_url = reverse_lazy('product_list')

    @method_decorator(login_required(login_url='login'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/products_list.html'
    context_object_name = 'products'
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        tag_id = self.kwargs.get('tag_id')

        if category_id:
            category = get_object_or_404(Category, id=category_id)
            queryset = queryset.filter(category=category)

        if tag_id:
            tag = get_object_or_404(Tag, id=tag_id)
            queryset = queryset.filter(tags=tag)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        context['categories'] = Category.objects.all()
        context['paginated_objects'] = paginate_objects(self.request, context['products'], self.paginate_by)
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


class ProductCreateView(CreateView):
    model = Product
    template_name = 'catalog/product_form.html'
    form_class = ProductForm
    success_url = reverse_lazy('product_list')

    @method_decorator(login_required(login_url='login'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'catalog/product_form.html'
    form_class = ProductForm
    success_url = reverse_lazy('product_list')

    @method_decorator(login_required(login_url='login'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_deleted = True
        self.object.save()
        return redirect(self.success_url)

    @method_decorator(login_required(login_url='login'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class OrderListView(ListView):
    model = Order
    template_name = 'catalog/orders_list.html'
    context_object_name = 'orders'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        context['categories'] = Category.objects.all()
        context['paginated_objects'] = paginate_objects(self.request, context['orders'], self.paginate_by)
        return context


class OrderDetailView(DetailView):
    model = Order
    template_name = 'catalog/order_detail.html'
    context_object_name = 'order'


class OrderCreateView(CreateView):
    model = Order
    template_name = 'catalog/order_form.html'
    form_class = OrderForm
    success_url = reverse_lazy('order_list')

    @method_decorator(login_required(login_url='login'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class OrderUpdateView(UpdateView):
    model = Order
    template_name = 'catalog/order_form.html'
    form_class = OrderForm
    success_url = reverse_lazy('order_list')

    @method_decorator(login_required(login_url='login'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class OrderDeleteView(DeleteView):
    model = Order
    template_name = 'catalog/order_confirm_delete.html'
    success_url = reverse_lazy('order_list')
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_deleted = True
        self.object.save()
        return redirect(self.success_url)

    @method_decorator(login_required(login_url='login'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


@login_required(login_url='login')
def api(request):
    return render(request, 'api/api.html')


def cart(request):
    return render(request, 'cart.html')


def feedback(request):
    # Логика страницы обратной связи
    return render(request, 'catalog/feedback.html')
