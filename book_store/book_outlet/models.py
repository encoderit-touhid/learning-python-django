from django.db import models
from django.core.validators import MaxLengthValidator,MinValueValidator
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=255)
    rating = models.IntegerField(validators=[MinValueValidator(1),MaxLengthValidator(5)])
    author = models.CharField(null=True, max_length=100)
    is_bestselling=models.BooleanField(default=False)
    slug = models.SlugField(default='', null=False, db_index=True)
    
    def get_single_permalink(self):
        return reverse('show', args=[self.slug])
    
    def save(self, *args, **kwargs):
        self.slug=slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"title: {self.title}, rating: {self.rating}, author: {self.author}, is_bestselling: {self.is_bestselling}"

    