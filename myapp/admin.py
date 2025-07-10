from django.contrib import admin
from.models import Book, Author, Publisher, Subject, User

# Register your models here.
# uv run python manage.py createsuperuser
# 123
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name']

@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'page_count', 'publisher']
    filter_horizontal = ['authors', 'subjects']  # Makes it easier to select multiple 

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'tokens']
    filter_horizontal = ['wish_list', 'shopping_cart']