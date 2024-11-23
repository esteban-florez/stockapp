from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Sum
from .models import Category, Supplier, Product, Movement

class UniqueNameForm(forms.Form):
  model = None

  def clean(self):
    cleaned_data = super().clean()
    name = cleaned_data.get('name')

    if name:
      if self.model.objects.filter(name=name).exists():
        error = ValidationError('Ya existe un registro con ese nombre.')

        self.add_error(field='name', error=error)
    else:
      return cleaned_data
  

class CategoryForm(UniqueNameForm):
  model = Category
  name = forms.CharField(max_length=20, required=True)
  description = forms.CharField(max_length=50, required=True)

class SupplierForm(UniqueNameForm):
  model = Supplier
  name = forms.CharField(max_length=20, required=True)
  description = forms.CharField(max_length=50, required=True)
  category = forms.ModelChoiceField(required=True, queryset=Category.objects)

class ProductForm(UniqueNameForm):
  model = Product
  name = forms.CharField(max_length=20, required=True)
  price = forms.FloatField(max_value=1000, min_value=0.01, required=True)
  description = forms.CharField(max_length=50, required=True)
  category = forms.ModelChoiceField(required=True, queryset=Category.objects)

class MovementForm(forms.Form):
  type = forms.ChoiceField(choices=[('plus', 'Ingreso'), ('minus', 'Salida')], required=True)
  amount = forms.IntegerField(min_value=1, required=True)
  reason = forms.CharField(max_length=30, required=False)
  product = forms.ModelChoiceField(
    required=True,
    queryset=Product.objects.annotate(stock=Sum('movement__amount')).filter(stock__gt=0)
  )
  supplier = forms.ModelChoiceField(required=False, queryset=Supplier.objects)
  
  def clean(self):
    cleaned_data = super().clean()

    type = cleaned_data.get('type')
    supplier = cleaned_data.get('supplier')
    missing_supplier = type == 'plus' and not supplier

    product = cleaned_data.get('product')
    amount = cleaned_data.get('amount')
    agg = Movement.objects.filter(product_id=product.id).aggregate(value=Sum('amount'))
    mov_sum = agg.get('value')
    exceeding_amount = amount and product and type == 'minus' and amount > mov_sum

    if missing_supplier:
      error = ValidationError('Si el tipo es ingreso, debes seleccionar un proveedor.')
      self.add_error(field='supplier', error=error)
    
    if exceeding_amount:
      error = ValidationError('La cantidad ingresada es mayor al stock disponible (max. %(stock)s).', params={ 'stock': mov_sum })
      self.add_error(field='amount', error=error)

    if not missing_supplier and not exceeding_amount:
      if type == 'minus':
        cleaned_data['amount'] = -cleaned_data['amount']
        del cleaned_data['supplier']

      del cleaned_data['type']
      return cleaned_data
