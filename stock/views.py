from .models import Product, Movement, Supplier, Category
from django.db.models import Sum
from django.views.generic.list import ListView
from django.shortcuts import render, redirect
from .forms import CategoryForm

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
  template_name = 'products.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['links'] = ['Productos', 'Lista de Productos']
    return context

class SupplierListView(LatestListView):
  model = Supplier
  template_name = 'suppliers.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['links'] = ['Proveedores', 'Lista de Proveedores']
    return context

class CategoryListView(LatestListView):
  model = Category
  template_name = 'categories.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['links'] = ['Categorías', 'Lista de Categorías']
    return context

def create_category(request):
  errors = session_errors(request)

  return render(request, 'create_category.html', {
    'links': ['Categorías', 'Registrar Categoría'],
    'errors': errors,
  })

def store_category(request):
  if not request.method == 'POST':
    return redirect('categories.create')

  form = CategoryForm(request.POST)

  if form.is_valid():
    Category.objects.create(**form.cleaned_data)
    return redirect('categories')
  else:
    request.session['errors'] = form.errors
    return redirect('categories.create')

def session_errors(request):
  if request.session.get('errors'):
    errors_copy = request.session['errors'].copy()
    del request.session['errors']
    return errors_copy
  else:
    return None
