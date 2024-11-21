from django.db import models

class TimeStampedModel(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
      abstract = True

class Category(TimeStampedModel):
  name = models.CharField(max_length=20)
  description = models.CharField(max_length=255)

  def __str__(self):
    return f"{self.name}"

class Product(TimeStampedModel):
  name = models.CharField(max_length=30)
  description = models.CharField(max_length=255)
  price = models.FloatField()
  category = models.ForeignKey(Category, on_delete=models.CASCADE)

  def __str__(self):
    return f"{self.name}"

class Supplier(TimeStampedModel):
  name = models.CharField(max_length=30)
  description = models.CharField(max_length=255)
  
  def __str__(self):
    return f"{self.name}"

class Movement(TimeStampedModel):
  amount = models.IntegerField()
  reason = models.CharField(max_length=30, null=True)
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True)

  def __str__(self):
    return f"{self.product.name} {self.amount}"
