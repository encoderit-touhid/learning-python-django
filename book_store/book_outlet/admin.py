from django.contrib import admin
from .models import Book, Author,Address,Country

# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_filter = ("rating", "is_bestselling", "author")
    list_display = ("title", "author", "is_bestselling", "rating", "slug")
    # readonly_fields=("slug",)
    prepopulated_fields={"slug":("title",)}
    
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name")
    search_fields = ("first_name", "last_name")

class AddressAdmin(admin.ModelAdmin):
    list_display = ("street", "city", "postcode", "country")
    list_filter = ("city", "country")
    search_fields = ("street", "city", "country", "postcode")

class CountryAdmin(admin.ModelAdmin):
    list_display = ("name", "code")
    list_filter = ("name", "code")
    search_fields = ("name", "code")

admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Country,CountryAdmin)
