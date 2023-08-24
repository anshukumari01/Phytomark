from django.contrib import admin
from .models import Products

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
  list_display = ('name', 'cas_number', 'cat_number', 'modified_date', 'stock', 'is_available')
  prepopulated_fields = {'slug':('name',)}

admin.site.register(Products, ProductAdmin)