from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from MainApp import views
from MainApp.api_views import CategoryViewSet, TagViewSet, ProductViewSet, OrderViewSet, OrderItemViewSet
from MainApp.views import ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView, \
    CategoryListView, CategoryDetailView, CategoryCreateView, TagListView, TagDetailView, TagCreateView, OrderListView, \
    OrderDetailView, OrderCreateView, OrderDeleteView, OrderUpdateView, RegisterView, user_profile

schema_view = get_schema_view(
    openapi.Info(
        title="MainApp API",
        default_version='v1',
        description="MainApp API used for practical work #3",
        contact=openapi.Contact(email="igorpheik@gmail.com"),
        license=openapi.License(name="MPT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

catalog = [
    path('categories', CategoryListView.as_view(), name='categories_list'),
    path('category/<int:pk>', CategoryDetailView.as_view(), name='category_detail'),
    path('category/create', CategoryCreateView.as_view(), name='category_create'),

    path('tags', TagListView.as_view(), name='tags_list'),
    path('tag/<int:pk>', TagDetailView.as_view(), name='tag_detail'),
    path('tag/create', TagCreateView.as_view(), name='tag_create'),

    path('products', ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>', ProductDetailView.as_view(), name='product_detail'),
    path('product/create/', ProductCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('products/category/<int:category_id>/', ProductListView.as_view(), name='product_list_by_category'),
    path('products/tag/<int:tag_id>/', ProductListView.as_view(), name='product_list_by_tag'),

    path('orders', OrderListView.as_view(), name='order_list'),
    path('order/<uuid:pk>', OrderDetailView.as_view(), name='order_detail'),
    path('order/create/', OrderCreateView.as_view(), name='order_create'),
    path('order/<uuid:pk>/delete/', OrderDeleteView.as_view(), name='order_delete'),
    path('order/<uuid:pk>/update/', OrderUpdateView.as_view(), name='order_update'),

    path('feedback/', views.feedback, name='feedback'),
]

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'orderitems', OrderItemViewSet, basename='orderitem')

urlpatterns = [
    path('', views.home, name='home'),

    path('catalog/', include(catalog)),

    path('cart/', views.cart, name='cart'),

    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', user_profile, name='user_profile'),

    path('api/', views.api, name='api'),
    path('api/', include(router.urls)),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
]
