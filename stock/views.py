from .models import Product
from django.db.models import Sum
from django.shortcuts import render

def index(request):
  products = Product.objects.order_by('-created_at').annotate(stock=Sum('movement__amount'))
  links = ['Inicio', 'Estado de Inventario']
  
  return render(request, 'index.html', {
    'products': products,
    'links': links
  })
