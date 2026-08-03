from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse
from .models import Book,Author
from django.db.models import Avg,Max,Min
from django.template.context_processors import request
from django.db import connection, reset_queries
# Create your views here.
from book_outlet.models import Country

def index(request):
    books=Book.objects.all().order_by('title')
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

def test(request):
    books=Book.objects.all().order_by('title')
    output = []
    for book in books:
        if book.author:
            output.append(f"{book.title}: {book.author.first_name} {book.author.last_name}")
    output.append(f"Current SQL is {books.query}")
    books=Book.objects.filter(author__first_name__contains="Touhid")
    output.append(f"SQL after filtering is {books.query}")
    author=Author.objects.filter(first_name__contains="Touhid").first()
    if author:
        output.append(f"Found author: {author.first_name} {author.last_name}")
        output.append(f"Books of this author {author.first_name} {author.last_name}:")
       # author_books = author.book_set.all() [if no related Name]
        author_books = author.books.all()
        for b in author_books:
            output.append(f"- {b.title} (Rating: {b.rating})")
    country = Country.objects.filter(code="BD").first()
    if country:
        book_related_to_country = country.book_set.all()
        if book_related_to_country:
            for single_book in book_related_to_country:
                output.append(f"Found Country: {country.name} {country.code}")
                output.append(f"Book: {single_book.title} (Rating: {single_book.rating})")       
    return HttpResponse("<br>".join(output) if output else "No books found.")



def n_plus_one_demo(request):
    reset_queries()
    
    # -------------------------------------------------------------
    # 1. BAD APPROACH (N+1 Query Problem)
    # -------------------------------------------------------------
    # Fetching 50 books = 1 query
    # Accessing book.author for each book = 50 additional queries
    # Accessing book.published_countries = 50 additional queries
    bad_books = Book.objects.all()[:10]
    bad_output = []
    for book in bad_books:
        author_name = f"{book.author.first_name} {book.author.last_name}"
        countries = ", ".join([c.name for c in book.published_countries.all()])
        bad_output.append(f"Book: {book.title} | Author: {author_name} | Countries: {countries}")
        
    bad_query_count = len(connection.queries)
    bad_queries_log = [q['sql'] for q in connection.queries]
    
    reset_queries()
    
    # -------------------------------------------------------------
    # 2. GOOD APPROACH (Optimized: No N+1 Problem)
    # -------------------------------------------------------------
    # select_related('author'): SQL JOIN for ForeignKey (Author) -> 0 extra queries
    # prefetch_related('published_countries'): Separate query for ManyToMany -> 1 extra query
    good_books = Book.objects.select_related('author').prefetch_related('published_countries')[:10]
    good_output = []
    for book in good_books:
        author_name = f"{book.author.first_name} {book.author.last_name}"
        countries = ", ".join([c.name for c in book.published_countries.all()])
        good_output.append(f"Book: {book.title} | Author: {author_name} | Countries: {countries}")
        
    good_query_count = len(connection.queries)
    good_queries_log = [q['sql'] for q in connection.queries]
    
    html = f"""
    <h2>N+1 Query Problem Demo</h2>
    
    <h3 style="color: red;">1. Without Optimization (N+1 Problem)</h3>
    <p><b>Executed Query Count:</b> {bad_query_count} queries</p>
    <ul>
        {"".join([f"<li>{item}</li>" for item in bad_output])}
    </ul>
    
    <h3 style="color: green;">2. With Optimization (select_related + prefetch_related)</h3>
    <p><b>Executed Query Count:</b> {good_query_count} queries</p>
    <ul>
        {"".join([f"<li>{item}</li>" for item in good_output])}
    </ul>
    
    <h3>Queries Executed in Optimized Version:</h3>
    <ol>
        {"".join([f"<li><code>{sql}</code></li>" for sql in good_queries_log])}
    </ol>
    """
    return HttpResponse(html)

def field_selection_demo(request):
    reset_queries()
    
    # -------------------------------------------------------------------------
    # 1. SELECT ONLY SPECIFIC FIELDS using only()
    # Generates: SELECT id, title, rating FROM book_outlet_book ...
    # -------------------------------------------------------------------------
    books_only = Book.objects.only('title', 'rating')[:5]
    only_sql = str(books_only.query)
    
    # -------------------------------------------------------------------------
    # 2. DEFER (EXCLUDE) HEAVY OR UNNEEDED FIELDS using defer()
    # Generates: SELECT all fields EXCEPT 'slug' and 'is_bestselling' ...
    # -------------------------------------------------------------------------
    books_defer = Book.objects.defer('slug', 'is_bestselling')[:5]
    defer_sql = str(books_defer.query)

    # -------------------------------------------------------------------------
    # 3. RETURN DICTIONARIES INSTEAD OF MODEL OBJECTS using values()
    # Useful for fast APIs / JSON serialization (skips model instantiation overhead)
    # -------------------------------------------------------------------------
    books_dict = list(Book.objects.values('title', 'rating')[:5])
    
    # -------------------------------------------------------------------------
    # 4. RETURN TUPLES OR FLAT LISTS using values_list()
    # flat=True works when selecting a single field to get a clean Python list: ['1984', 'Dune', ...]
    # -------------------------------------------------------------------------
    book_titles_list = list(Book.objects.values_list('title', flat=True)[:5])

    html = f"""
    <h2>Django Query Optimization: Field Selection</h2>
    
    <h3 style="color: blue;">1. only('title', 'rating')</h3>
    <p>Fetches only specified columns as model instances. Extra fields loaded lazily if accessed.</p>
    <pre><b>Generated SQL:</b><br>{only_sql}</pre>
    
    <h3 style="color: purple;">2. defer('slug', 'is_bestselling')</h3>
    <p>Fetches all fields EXCEPT the deferred ones.</p>
    <pre><b>Generated SQL:</b><br>{defer_sql}</pre>
    
    <h3 style="color: green;">3. values('title', 'rating')</h3>
    <p>Returns dictionaries instead of model objects (faster & lighter):</p>
    <pre>{books_dict}</pre>
    
    <h3 style="color: darkorange;">4. values_list('title', flat=True)</h3>
    <p>Returns a flat list of values:</p>
    <pre>{book_titles_list}</pre>
    """
    return HttpResponse(html)

def many_to_many(request):
    countries_data = [
        {
           'slug': "harry-potter-and-the-philosophers-stone",
           'name': "Bangladesh",
            'code': "BD"
        },
        {
           'slug': "harry-potter-and-the-philosophers-stone",
           'name': "United States",
            'code': "US"
        },
        {
             'slug': "harry-potter-and-the-chamber-of-secrets",
             'name': "United Kingdom",
              'code': "GB"
        },
        {
             'slug': "harry-potter-and-the-chamber-of-secrets",
             'name': "Bangladesh", 
             'code': "BD"
        },
        {
            'slug': "harry-potter-and-the-prisoner-of-azkaban",
            'name': "Canada",
            'code': "CA"
        },
        {
             'slug': "harry-potter-and-the-prisoner-of-azkaban",
             'name': "India", 
             'code': "IN"
        }
    ]
    
    output = []
    for item in countries_data:
        # 1. Get or create the Country in database
        country, _ = Country.objects.get_or_create(
            name=item['name'], 
            code=item['code']
        )
        
        # 2. Get the specific Book instance by slug
        book = Book.objects.filter(slug=item['slug']).first()
        
        # 3. Add country to book's ManyToMany relation
        if book:
            book.published_countries.add(country)
            output.append(f"Added {country.name} to '{book.title}'")

    return HttpResponse("<br>".join(output) if output else "No updates made.")