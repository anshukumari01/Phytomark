from django.db import models

# Create your models here.

class Banner(models.Model):
  name = models.TextField(max_length=30, blank=True)
  link = models.URLField(max_length=500, blank=True)
  tagline = models.TextField(max_length=160, blank=True)
  description = models.TextField(max_length=1255, blank=True)
  image = models.ImageField(upload_to='images/banner', blank=True)

  def __str__(self):
    return self.name

class Placeholder(models.Model):
  name = models.TextField(max_length=30, blank=True)
  link = models.URLField(max_length=200, blank=True)
  description = models.TextField(max_length=1255, blank=True)
  image = models.ImageField(upload_to='images/placeholder', blank=True)

  def __str__(self):
    return self.name

class About(models.Model):
  name = models.TextField(max_length=30, blank=True)
  description = models.TextField(max_length=1000, blank=True)


  class Meta:
    verbose_name = 'about'
    verbose_name_plural = 'about'

  def __str__(self):
    return self.name


class Fproduct(models.Model):
  name = models.TextField(max_length=30, blank=True)
  link = models.URLField(max_length=500, blank=True)
  image = models.ImageField(upload_to='images/product', blank=True)

  def __str__(self):
    return self.name
  
class Info(models.Model):
  name = models.TextField(max_length=20, blank=True )
  address1 = models.TextField(max_length=100, blank=True)
  address2 = models.TextField(max_length=100, blank=True)
  phone_no = models.CharField(max_length=20, blank=True)
  email = models.EmailField(max_length=254, unique=True)
  

  def __str__(self):
    return self.name
  
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.TextField()
    message = models.TextField()

    def __str__(self):
        return self.name
  
class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1255, blank=True)
    image = models.ImageField(upload_to='images/placeholder', blank=True)

    def __str__(self):
        return self.name
  
class OrganicFarming(models.Model):
    name = models.CharField(max_length=100, null=True)
    description = models.TextField(max_length=1255, blank=True)
    image = models.ImageField(upload_to='images/placeholder', blank=True)

    def __str__(self):
        return self.name
  
