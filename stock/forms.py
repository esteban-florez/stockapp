from django import forms
from django.core.exceptions import ValidationError
from .models import Category

class UniqueNameForm(forms.Form):
  model = None

  def clean(self):
    cleaned_data = super().clean()
    name = cleaned_data.get('name')

    if name:
      if self.model.objects.filter(name=name).exists():
        error = ValidationError('El campo %(value)s ya fué registrado.', params={
          'value': 'nombre',
        })

        self.add_error(field='name', error=error)
    else:
      return cleaned_data
  

class CategoryForm(UniqueNameForm):
  model = Category
  name = forms.CharField(max_length=20)
  description = forms.CharField(max_length=50)
