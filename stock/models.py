from django.db import models

class TimeStampedModel(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
      abstract = True

class Category(TimeStampedModel):
  name = models.CharField(max_length=20, unique=True)
  description = models.CharField(max_length=50)

  def __str__(self):
    return f"{self.name}"

class Product(TimeStampedModel):
  name = models.CharField(max_length=20, unique=True)
  description = models.CharField(max_length=50)
  price = models.FloatField()
  category = models.ForeignKey(Category, on_delete=models.CASCADE)

  def __str__(self):
    return f"{self.name}"

class Supplier(TimeStampedModel):
  name = models.CharField(max_length=20, unique=True)
  description = models.CharField(max_length=50)
  category = models.ForeignKey(Category, on_delete=models.CASCADE)

  def __str__(self):
    return f"{self.name}"

class Movement(TimeStampedModel):
  amount = models.IntegerField()
  reason = models.CharField(max_length=30, null=True)
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True)
  
  @property
  def type(self):
    if self.amount > 0:
      return 'Ingreso'

    return 'Salida'

  @property
  def famount(self):
    return f"+{self.amount}" if self.type == 'Ingreso' else f"{self.amount}"

  @property
  def supplier_name(self):
    return 'N/A' if self.supplier == None else self.supplier.name

  def __str__(self):
    return f"{self.product.name} {self.amount}"
