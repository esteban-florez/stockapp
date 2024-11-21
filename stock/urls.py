from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('movements', views.MovementListView.as_view(), name='movements'),
    path('products', views.ProductListView.as_view(), name='products'),
]
