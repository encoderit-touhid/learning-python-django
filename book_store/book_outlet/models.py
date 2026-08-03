from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.

class Country(models.Model):
      name=models.CharField(max_length=250)
      code=models.CharField(max_length=10)
      def __str__(self):
        return f"{self.name}, {self.code}"
      class Meta:
        # db_table = ''
        # managed = True
        verbose_name = 'Country'
        verbose_name_plural = 'Country'
class Address(models.Model):
    street=models.CharField(max_length=255)
    postcode=models.CharField(max_length=255)
    city=models.CharField(max_length=255)
    country=models.CharField(max_length=255)
    def __str__(self):
        return f"{self.street}, {self.city}, {self.postcode}, {self.country}"
    class Meta:
        # db_table = ''
        # managed = True
        verbose_name = 'Address'
        verbose_name_plural = 'Address Entries'

class Author(models.Model):
    first_name = models.CharField(max_length=255)
    last_name  = models.CharField(max_length=255)
    address    = models.OneToOneField(Address,on_delete=models.CASCADE,null=True)
    def __str__(self):
     return f"first_name: {self.first_name}, last_name: {self.last_name}"  
class Book(models.Model):
    title = models.CharField(max_length=255)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    # author = models.CharField(null=True, max_length=100)
   # author = models.ForeignKey(Author,on_delete=models.CASCADE)
    author = models.ForeignKey(Author,on_delete=models.CASCADE,related_name="books")
    is_bestselling=models.BooleanField(default=False)
    # slug = models.SlugField(default='', editable=False, blank=True, null=False, db_index=True)
    slug = models.SlugField(default='',  null=False, db_index=True)
    
    published_countries=models.ManyToManyField(Country,null=False)
    
    def get_single_permalink(self):
        return reverse('show', args=[self.slug])
    
    # def save(self, *args, **kwargs):
    #     self.slug=slugify(self.title)
    #     super().save(*args, **kwargs)
    
    def __str__(self):
        # return f"title: {self.title}, rating: {self.rating}, author: {self.author}, is_bestselling: {self.is_bestselling}"
         return f"title: {self.title}, rating: {self.rating},  is_bestselling: {self.is_bestselling}"

    