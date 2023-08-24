from django.db import models
from django.db.models import Avg, Count
from autoslug import AutoSlugField
from django.urls import reverse
import uuid
# Create your models here.


class Products(models.Model):
  name = models.CharField(max_length=100, unique=True)
  slug = AutoSlugField(max_length=100, unique=True)
  mol_formula = models.CharField(max_length=100)
  synonyms = models.CharField(max_length=1000, blank=True, default=None)
  mol_weight = models.CharField(max_length=10, blank=True, default=None)
  cas_number = models.CharField(max_length=100)
  pack_size = models.CharField(max_length=100)
  price = models.PositiveIntegerField(default=None)
  
  cat_number = models.CharField(max_length=10, unique=True, default=uuid.uuid4, editable=False)
  stock = models.PositiveIntegerField(default=None)
  is_available = models.BooleanField(default=True)

  image = models.ImageField(upload_to='images/products', blank=True, default=None, null=True)

  description = models.TextField(max_length=2000, blank=True, default=None)
  create_date = models.DateTimeField(auto_now_add=True)
  modified_date = models.DateTimeField(auto_now=True)

  assay = models.CharField(max_length=100, blank=True, default=None)
  form = models.CharField(max_length=100, blank=True, default=None)
  manufacturer = models.CharField(max_length=100, blank=True, default=None)
  smiles_string =models.CharField(max_length=1000, blank=True, default=None)
  safety = models.TextField(max_length=2000, blank=True, null=True)
  GHSpictogram = models.CharField(max_length=10, null=True)
  HazardWarnings = models.CharField(max_length=100, null=True)
  SecutityInstructions = models.CharField(max_length=200, null=True)
  class Meta:
    verbose_name = 'Product'
    verbose_name_plural = 'Products'

  def get_url(self):
    return reverse('product-view', args=[self.slug])

  def __str__(self):
    return self.name
  

