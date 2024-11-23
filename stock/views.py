from .models import Product, Movement, Supplier, Category
from django.db.models import Sum
from django.views.generic.list import ListView
from django.shortcuts import render, redirect
from .forms import CategoryForm, SupplierForm, ProductForm, MovementForm
from .shortcuts import session_old, session_errors

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
    context['links'] = ['Movimientos', 'Lista de Movimientos']
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
  old = session_old(request)

  return render(request, 'create_category.html', {
    'links': ['Categorías', 'Registrar Categoría'],
    'errors': errors,
    'old': old,
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
    request.session['old'] = request.POST
    return redirect('categories.create')

def create_supplier(request):
  errors = session_errors(request)
  old = session_old(request)
  categories = Category.objects.all()

  return render(request, 'create_supplier.html', {
    'links': ['Proveedores', 'Registrar Proveedor'],
    'errors': errors,
    'old': old,
    'categories': categories,
  })

def store_supplier(request):
  if not request.method == 'POST':
    return redirect('suppliers.create')

  form = SupplierForm(request.POST)

  if form.is_valid():
    Supplier.objects.create(**form.cleaned_data)
    return redirect('suppliers')
  else:
    request.session['errors'] = form.errors
    request.session['old'] = request.POST
    return redirect('suppliers.create')

def create_product(request):
  errors = session_errors(request)
  old = session_old(request)
  categories = Category.objects.all()

  return render(request, 'create_product.html', {
    'links': ['Productos', 'Registrar Producto'],
    'errors': errors,
    'old': old,
    'categories': categories,
  })

def store_product(request):
  if not request.method == 'POST':
    return redirect('products.create')

  form = ProductForm(request.POST)

  if form.is_valid():
    Product.objects.create(**form.cleaned_data)
    return redirect('products')
  else:
    request.session['errors'] = form.errors
    request.session['old'] = request.POST
    return redirect('products.create')


def create_movement(request):
  errors = session_errors(request)
  old = session_old(request)
  queryset = Product.objects.annotate(stock=Sum('movement__amount')).filter(stock__gt=0)
  products = list(queryset.values('id', 'name', 'stock'))
  suppliers = Supplier.objects.all()

  return render(request, 'create_movement.html', {
    'links': ['Movimientos', 'Registrar Movimiento'],
    'errors': errors,
    'old': old,
    'products': products,
    'suppliers': suppliers,
  })

def store_movement(request):
  if not request.method == 'POST':
    return redirect('movements.create')

  form = MovementForm(request.POST)

  if form.is_valid():
    Movement.objects.create(**form.cleaned_data)
    return redirect('movements')
  else:
    request.session['errors'] = form.errors
    request.session['old'] = request.POST
  return redirect('movements.create')

