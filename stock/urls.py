from django.urls import path
from . import views

urlpatterns = [
    path('', views.StockListView.as_view(), name='index'),
    path('movements', views.MovementListView.as_view(), name='movements'),
    path('products', views.ProductListView.as_view(), name='products'),
    path('suppliers', views.SupplierListView.as_view(), name='suppliers'),
    path('categories', views.CategoryListView.as_view(), name='categories'),
]
