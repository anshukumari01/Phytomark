from django.db import models

# Create your models here.
class Carousel(models.Model):
  name = models.TextField(max_length=30, blank=True)
  image = models.ImageField(upload_to='images/about', blank=True)

  def __str__(self):
    return self.name
  
class Aboutus(models.Model):
  name = models.TextField(max_length=30, blank=True)
  discription1 = models.TextField(max_length=1000, blank=True)
  discription2 = models.TextField(max_length=1000, blank=True)
  discription3 = models.TextField(max_length=1000, blank=True)
  
  class Meta:
    verbose_name = 'aboutus'
    verbose_name_plural = 'aboutus'

  def __str__(self):
    return self.name
  
class Seperation(models.Model):
  name = models.TextField(max_length=50, blank=True)
  discription = models.TextField(max_length=2000, blank=True)
  image = models.ImageField(upload_to='images/about', blank=True)

  def __str__(self):
    return self.name