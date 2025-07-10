from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
# uv run python manage.py makemigrations
# uv run python manage.py migrate
# when DB is changed, updates

class Subject(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Publisher(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=300)
    cover_image = models.CharField(max_length=200)
    page_count = models.IntegerField()
    authors = models.ManyToManyField(Author, related_name='books')
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, related_name='books')
    subjects = models.ManyToManyField(Subject, related_name='books')
    summary = models.CharField(max_length=1600)
    downloads = models.IntegerField()
    cost = models.IntegerField()

    
    def __str__(self):
        return self.title
    

class User(AbstractUser):
    email = models.EmailField(unique=True)
    tokens = models.IntegerField(default=0)
    wish_list = models.ManyToManyField(Book, blank=True, related_name='wishlisted_by')
    shopping_cart = models.ManyToManyField(Book, blank=True, related_name='in_cart_of')
    
    # Use email as the login field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def add_tokens(self, amount):
        """Add tokens to user account"""
        self.tokens += amount
        self.save()
    
    def spend_tokens(self, amount):
        """Spend tokens if user has enough"""
        if self.tokens >= amount:
            self.tokens -= amount
            self.save()
            return True
        return False
    
    def add_to_wishlist(self, book):
        self.wish_list.add(book)

    def add_to_cart(self, book):
        self.shopping_cart.add(book)
    
    def remove_from_wishlist(self, book):
        self.wish_list.remove(book)

    def remove_from_cart(self, book):
        self.shopping_cart.remove(book)
    
    def get_wishlist(self):
        return self.wish_list.all()
    
    def get_cart(self):
        return self.shopping_cart.all()
    
    def __str__(self):
        return self.email