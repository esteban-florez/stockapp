from django.urls import path
from . import views

urlpatterns = [
    path('', views.StockListView.as_view(), name='index'),
    path('movements', views.MovementListView.as_view(), name='movements'),
    path('movements/create', views.create_movement, name='movements.create'),
    path('movements/store', views.store_movement, name='movements.store'),
    path('products', views.ProductListView.as_view(), name='products'),
    path('products/create', views.create_product, name='products.create'),
    path('products/store', views.store_product, name='products.store'),
    path('products/<int:product_id>/edit', views.edit_product, name='products.edit'),
    path('products/<int:product_id>/update', views.update_product, name='products.update'),
    path('suppliers', views.SupplierListView.as_view(), name='suppliers'),
    path('suppliers/create', views.create_supplier, name='suppliers.create'),
    path('suppliers/store', views.store_supplier, name='suppliers.store'),
    path('suppliers/<int:supplier_id>/edit', views.edit_supplier, name='suppliers.edit'),
    path('suppliers/<int:supplier_id>/store', views.update_supplier, name='suppliers.update'),
    path('categories', views.CategoryListView.as_view(), name='categories'),
    path('categories/create', views.create_category, name='categories.create'),
    path('categories/store', views.store_category, name='categories.store'),
    path('categories/<int:category_id>/edit', views.edit_category, name='categories.edit'),
    path('categories/<int:category_id>/update', views.update_category, name='categories.update'),
]
