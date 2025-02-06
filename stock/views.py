from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.http import HttpResponse, Http404
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_not_required
from django.urls import reverse
from django.views.generic.list import ListView
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
# from weasyprint import HTML
import pdfkit
# import os.path
from .forms import CategoryForm, SupplierForm, ProductForm, MovementForm, RegisterForm, LoginForm
from .models import Product, Movement, Supplier, Category, User
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
    sum_query = Coalesce(Sum('movement__amount'), 0)
    return super().get_queryset().annotate(stock=sum_query)

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
  action = reverse('categories.store')

  return render(request, 'create_category.html', {
    'links': ['Categorías', 'Registrar Categoría'],
    'errors': errors,
    'old': old,
    'action': action,
  })

def store_category(request):
  if not request.method == 'POST':
    return redirect('categories.create')

  form = CategoryForm(request.POST)

  if form.is_valid():
    Category.objects.create(**form.cleaned_data)
    messages.add_message(request, messages.SUCCESS, 'La categoría se ha registrado exitosamente.')
    return redirect('categories')

  request.session['errors'] = form.errors
  request.session['old'] = request.POST
  return redirect('categories.create')

def edit_category(request, category_id):
  category = get_object_or_404(Category, pk=category_id)
  errors = session_errors(request)
  old = session_old(request)
  action = reverse('categories.update', args=[category_id])

  return render(request, 'edit_category.html', {
    'links': ['Categorías', 'Editar Categoría'],
    'category': category,
    'errors': errors,
    'old': old,
    'action': action,
  })

def update_category(request, category_id):
  category = get_object_or_404(Category, pk=category_id)

  if not request.method == 'POST':
    return redirect('categories.edit', category_id=category.id)

  form = CategoryForm(request.POST, exclude=category_id)

  if form.is_valid():
    Category.objects.filter(id=category_id).update(**form.cleaned_data)
    messages.add_message(request, messages.SUCCESS, 'La categoría se actualizado exitosamente.')
    return redirect('categories')

  request.session['errors'] = form.errors
  request.session['old'] = request.POST
  return redirect('categories.edit', category_id=category.id)

def create_supplier(request):
  errors = session_errors(request)
  old = session_old(request)
  categories = Category.objects.all()
  action = reverse('suppliers.store')

  return render(request, 'create_supplier.html', {
    'links': ['Proveedores', 'Registrar Proveedor'],
    'errors': errors,
    'old': old,
    'categories': categories,
    'action': action,
  })

def store_supplier(request):
  if not request.method == 'POST':
    return redirect('suppliers.create')

  form = SupplierForm(request.POST)

  if form.is_valid():
    Supplier.objects.create(**form.cleaned_data)
    messages.add_message(request, messages.SUCCESS, 'El proveedor se ha creado exitosamente.')
    return redirect('suppliers')

  request.session['errors'] = form.errors
  request.session['old'] = request.POST
  return redirect('suppliers.create')


def edit_supplier(request, supplier_id):
  supplier = get_object_or_404(Supplier, pk=supplier_id)
  errors = session_errors(request)
  old = session_old(request)
  categories = Category.objects.all()
  action = reverse('suppliers.update', args=[supplier_id])

  return render(request, 'edit_supplier.html', {
    'links': ['Proveedores', 'Editar Proveedor'],
    'supplier': supplier,
    'errors': errors,
    'old': old,
    'action': action,
    'categories': categories,
  })

def update_supplier(request, supplier_id):
  supplier = get_object_or_404(Supplier, pk=supplier_id)

  if not request.method == 'POST':
    return redirect('suppliers.edit', supplier_id=supplier.id)

  form = SupplierForm(request.POST, exclude=supplier_id)

  if form.is_valid():
    Supplier.objects.filter(id=supplier_id).update(**form.cleaned_data)
    messages.add_message(request, messages.SUCCESS, 'El proveedor se ha actualizado exitosamente.')
    return redirect('suppliers')

  request.session['errors'] = form.errors
  request.session['old'] = request.POST
  return redirect('suppliers.edit', supplier_id=supplier.id)

def create_product(request):
  errors = session_errors(request)
  old = session_old(request)
  categories = Category.objects.all()
  action = reverse('products.store')

  return render(request, 'create_product.html', {
    'links': ['Productos', 'Registrar Producto'],
    'errors': errors,
    'old': old,
    'categories': categories,
    'action': action,
  })

def store_product(request):
  if not request.method == 'POST':
    return redirect('products.create')

  form = ProductForm(request.POST)

  if form.is_valid():
    Product.objects.create(**form.cleaned_data)
    messages.add_message(request, messages.SUCCESS, 'El producto se ha registrado exitosamente.')
    return redirect('products')

  request.session['errors'] = form.errors
  request.session['old'] = request.POST
  return redirect('products.create')

def edit_product(request, product_id):
  product = get_object_or_404(Product, pk=product_id)
  errors = session_errors(request)
  old = session_old(request)
  categories = Category.objects.all()
  action = reverse('products.update', args=[product_id])

  return render(request, 'edit_product.html', {
    'links': ['Productos', 'Editar Producto'],
    'product': product,
    'errors': errors,
    'old': old,
    'action': action,
    'categories': categories,
  })

def update_product(request, product_id):
  product = get_object_or_404(Product, pk=product_id)

  if not request.method == 'POST':
    return redirect('products.edit', product_id=product.id)

  form = ProductForm(request.POST, exclude=product_id)

  if form.is_valid():
    Product.objects.filter(id=product_id).update(**form.cleaned_data)
    messages.add_message(request, messages.SUCCESS, 'El producto se ha actualizado exitosamente.')
    return redirect('products')

  request.session['errors'] = form.errors
  request.session['old'] = request.POST
  return redirect('products.edit', product_id=product.id)

def create_movement(request):
  errors = session_errors(request)
  old = session_old(request)
  sum_query = Coalesce(Sum('movement__amount'), 0)
  queryset = Product.objects.annotate(stock=sum_query).filter(stock__gt=0)
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
    messages.add_message(request, messages.SUCCESS, 'El movimiento se ha registrado exitosamente.')
    return redirect('movements')

  request.session['errors'] = form.errors
  request.session['old'] = request.POST
  return redirect('movements.create')

def inventory_pdf(request):
  sum_query = Coalesce(Sum('movement__amount'), 0)
  products = Product.objects.order_by('-created_at').annotate(stock=sum_query)

  template = render_to_string('pdf.html', {
    'product_list': products,
  })

  # Configuración de PDFKit (opcional)

  # config = pdfkit.configuration(wkhtmltopdf='wkhtmltopdf.exe') # Ajusta la ruta si es necesario

  # Generación del PDF con PDFKit
  pdf = pdfkit.from_string(template, False) # El segundo argumento es False para devolver el PDF como bytes
  # pdf = HTML(string=template).write_pdf()

  response = HttpResponse(pdf, content_type='application/pdf')

  response['Content-Disposition'] = 'filename="Inventario.pdf"'
  return response

@login_not_required
def login(request):
  if request.method != 'POST' and request.method != 'GET':
    return Http404()
  
  if request.user.is_authenticated:
    return redirect('index')

  if request.method == 'GET':
    errors = session_errors(request)
    old = session_old(request)

    return render(request, 'login.html', {
      'errors': errors,
      'old': old,
    })

  form = LoginForm(request.POST)

  if form.is_valid():
    user = auth.authenticate(request, **form.cleaned_data)
    if user:
      auth.login(request, user)
      return redirect('index')

    form.add_credentials_error()

  request.session['errors'] = form.errors
  request.session['old'] = request.POST
  return redirect('login')

@login_not_required
def register(request):
  if request.method != 'POST' and request.method != 'GET':
    return Http404()
  
  if request.user.is_authenticated:
    return redirect('index')

  if request.method == 'GET':
    errors = session_errors(request)
    old = session_old(request)

    return render(request, 'register.html', {
      'errors': errors,
      'old': old,
    })

  form = RegisterForm(request.POST)

  if form.is_valid():
    user = User.objects.create_user(**form.cleaned_data)
    auth.login(request, user)
    return redirect('index')

  request.session['errors'] = form.errors
  request.session['old'] = request.POST
  return redirect('register')

def logout(request):
  if request.method != 'POST':
    return Http404()

  auth.logout(request)
  return redirect('login')
