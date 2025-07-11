from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('books/', views.book_list, name="book_list"),
    path('books/<int:book_id>/', views.book_detail, name="book_detail"),
    path('register/', views.SignUpView.as_view(), name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('ajax/add-to-cart/', views.add_to_cart_ajax, name='add_to_cart_ajax'),
    path('ajax/add-to-wishlist/', views.add_to_wishlist_ajax, name='add_to_wishlist_ajax'),
    path('ajax/remove-from-cart/', views.remove_from_cart_ajax, name='remove_from_cart_ajax'),
    path('ajax/remove-from-wishlist/', views.remove_from_wishlist_ajax, name='remove_from_wishlist_ajax'),
    path('ajax/clear-wishlist/', views.clear_wishlist_ajax, name='clear_wishlist_ajax'),
    path('ajax/clear-cart/', views.clear_cart_ajax, name='clear_cart_ajax')
]


# urlpatterns = [
#     path('signup/', views.SignUpView.as_view(), name='signup'),
#     path('login/', views.CustomLoginView.as_view(), name='login'),
#     path('logout/', LogoutView.as_view(), name='logout'),
#     # Function-based alternatives:
#     # path('signup/', views.signup_view, name='signup'),
#     # path('login/', views.login_view, name='login'),
# ]