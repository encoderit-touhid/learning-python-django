from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Book
from django.db.models import Avg,Max,Min
# Create your views here.

def index(request):
    books=Book.objects.all()
    no_of_books=books.count()
    average_rating=books.aggregate(Avg("rating"),Max("rating"),Min("rating"))
    return render(request,"book_outlet/index.html",{"books":books,"total_number":no_of_books,"average_rating":average_rating})

def show(request, slug):
    try:
        book = Book.objects.get(slug=slug)
    except:
        raise Http404
    return render(request, "book_outlet/single-book.html", {"book": book})

def generate_slug(request):
    books=Book.objects.all()
    for book in books:
            book.save()        
    return render(request,"book_outlet/index.html",{"books":books})