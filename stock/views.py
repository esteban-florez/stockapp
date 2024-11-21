from .models import Product, Movement, Supplier, Category
from django.db.models import Sum
from django.views.generic.list import ListView

class LatestListView(ListView):
  class Meta:
    abstract = True

  def get_queryset(self):
    return super().get_queryset().order_by('-created_at')

class StockListView(LatestListView):
  model = Product
  template_name = 'index.html'
  
  def get_queryset(self):
    return super().get_queryset().annotate(stock=Sum('movement__amount'))

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['links'] = ['Inicio', 'Estado de Inventario']
    return context

class MovementListView(LatestListView):
  model = Movement
  template_name = 'movements.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['links'] = ['Inicio', 'Historial de Inventario']
    return context

class ProductListView(LatestListView):
  model = Product
  template_name = "products.html"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['links'] = ['Productos', 'Lista de Productos']
    return context

class SupplierListView(LatestListView):
  model = Supplier
  template_name = "suppliers.html"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['links'] = ['Proveedores', 'Lista de Proveedores']
    return context

class CategoryListView(LatestListView):
  model = Category
  template_name = "categories.html"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['links'] = ['Categorías', 'Lista de Categorías']
    return context


