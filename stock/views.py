from django.shortcuts import render
from django.http import HttpResponse

def index(request):
  return render(request, 'index.html', {
    'links': ['Inicio', 'Existencia de Inventario'],
  })
