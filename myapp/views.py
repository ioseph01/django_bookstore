from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.db.models import Q
from .models import Book

# Create your views here.

def home(request):

    # Get Top 10 books by downloads
    top_books = Book.objects.order_by('-downloads')[:10]
    context = {
        'books': top_books,
    }
        
    return render(request, 'home.html', context)


def about(request):
    return render(request, "about.html")


def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    # Get related books by shared subjects
    related_books = Book.objects.filter(
        subjects__in=book.subjects.all()
    ).exclude(id=book.id).distinct()[:15]

    context = {
        'book': book,
        'related_books': related_books,
        'in_cart': False,
        'in_wishlist': False
    }

    if request.user.is_authenticated:
        context['in_cart'] = request.user.shopping_cart.filter(pk=book.pk).exists()
        context['in_wishlist'] = request.user.wish_list.filter(pk=book.pk).exists()
        
        
    return render(request, 'book_detail.html', context)

from django.core.paginator import Paginator

def book_list(request):
    books = Book.objects.all()
    query = request.GET.get('q')
    sort = request.GET.get('sort', '')

    if query:
        books = books.filter(
            Q(title__icontains=query) | 
            Q(authors__first_name__icontains=query) |  # Search through author names
            Q(authors__last_name__icontains=query) |  # Search through author names
            Q(publisher__name__icontains=query) | # Search through publisher name
            Q(subjects__name__icontains=query)
        ).distinct()  # Remove duplicates from joins

    if sort == 'cost_asc':
        books = books.order_by('cost')
    elif sort == 'cost_desc':
        books = books.order_by('-cost')
    elif sort == 'downloads_asc':
        books = books.order_by('downloads')
    elif sort == 'downloads_desc':
        books = books.order_by('-downloads')
    elif sort == 'page_count_asc':
        books = books.order_by('page_count')
    elif sort == 'page_count_desc':
        books = books.order_by('-page_count')
    elif sort == 'title_asc':
        books = books.order_by('title')
    elif sort == 'title_desc':
        books = books.order_by('-title')

    paginator = Paginator(books, 20)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    return render(request, 'books.html', {
        'page_obj': page_obj,
        'books': page_obj,
        'query': query,
        
    })


from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Account created successfully! Please log in.')
        return response

class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'login.html'
    
    def get_success_url(self):
        return reverse_lazy('dashboard')  # Redirect after login

# Function-based view alternative
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Give new users 100 tokens
            user.tokens = 100
            user.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

from django.http import JsonResponse


@require_POST
@login_required
def add_to_cart_ajax(request):
    book_id = request.POST.get('book_id')
    if book_id:
        book = Book.objects.filter(id=book_id).first()
        if book:
            if book in request.user.shopping_cart.all():
                return JsonResponse({
                    'success': False,
                    'message': 'Book is already in cart',
                    'already_in_cart': True
                })
            request.user.add_to_cart(book)
            return JsonResponse({
                'success': True,
                'message': 'Added to cart',
                'book': {
                    'id': book.id,
                    'title': book.title,
                    'cost': float(book.cost),  # Ensure it's JSON-serializable
                    'authors': [
                        {
                            'first_name': author.first_name,
                            'last_name': author.last_name
                        }
                        for author in book.authors.all()
                    ]
                }
            })

            # return JsonResponse({'success': True, 'message': 'Added to cart', 'book': book})
    return JsonResponse({'success': False, 'message': 'Invalid book ID'})

@require_POST
@login_required
def add_to_wishlist_ajax(request):
    book_id = request.POST.get('book_id')
    if book_id:
        book = Book.objects.filter(id=book_id).first()
        if book:
            if book in request.user.wish_list.all():
                return JsonResponse({
                    'success': False,
                    'message': 'Book is already in wishlist',
                    'already_in_wishlist': True
                })
            request.user.add_to_wishlist(book)
            return JsonResponse({
                'success': True,
                'message': 'Added to wishlist',
                'book': {
                    'id': book.id,
                    'title': book.title,
                    'cost': float(book.cost),  # Ensure it's JSON-serializable
                    'authors': [
                        {
                            'first_name': author.first_name,
                            'last_name': author.last_name
                        }
                        for author in book.authors.all()
                    ]
                }
            })
    return JsonResponse({'success': False, 'message': 'Invalid book ID'})

@require_POST
@login_required
def remove_from_cart_ajax(request):
    book_id = request.POST.get('book_id')
    if book_id:
        book = Book.objects.filter(id=book_id).first()
        if book:
            request.user.remove_from_cart(book)
            return JsonResponse({'success': True, 'message': 'Removed from cart'})
    return JsonResponse({'success': False, 'message': 'Invalid book ID'})

@require_POST
@login_required
def remove_from_wishlist_ajax(request):
    book_id = request.POST.get('book_id')
    if book_id:
        book = Book.objects.filter(id=book_id).first()
        if book:
            request.user.remove_from_wishlist(book)
            return JsonResponse({'success': True, 'message': 'Removed from wishlist'})
    return JsonResponse({'success': False, 'message': 'Invalid book ID'})



@require_POST
@login_required
def clear_wishlist_ajax(request):
    if request.user.wish_list.exists():
        request.user.clear_wish_list()
        return JsonResponse({'success': True, 'message': 'Wishlist cleared.'})
    return JsonResponse({'success': False, 'message': 'Wishlist was already empty.'})

@require_POST
@login_required
def clear_cart_ajax(request):
    if request.user.shopping_cart.exists():
        request.user.clear_cart()
        return JsonResponse({'success': True, 'message': 'Cart cleared.'})
    return JsonResponse({'success': False, 'message': 'Cart was already empty.'})



@login_required
def dashboard_view(request):
    cart = request.user.get_cart()
    wishlist = request.user.get_wishlist()
    return render(request, "dashboard.html", {'cart': cart, 'wish_list': wishlist})

# @login_required
# def remove_from_cart(request, book_id):
#     book = get_object_or_404(Book, id=book_id)
#     request.user.remove_from_cart(book)
#     return JsonResponse({'success': True})

# @login_required
# def remove_from_wishlist(request, book_id):
#     book = get_object_or_404(Book, id=book_id)
#     request.user.remove_from_wishlist(book)
#     return JsonResponse({'success': True})
