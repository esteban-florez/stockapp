from .models import Product, Movement
from django.db.models import Sum
from django.shortcuts import render
from django.views.generic.list import ListView

class LatestListView(ListView):
  class Meta:
    abstract = True

  def get_queryset(self):
    return super().get_queryset().order_by('-created_at')

def index(request):
  products = Product.objects.annotate(stock=Sum('movement__amount')).order_by('-created_at')
  links = ['Inicio', 'Estado de Inventario']
  
  return render(request, 'index.html', {
    'products': products,
    'links': links
  })
  
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
  
