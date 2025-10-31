from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    # Auth
    path('register/', views.register_user, name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Books
    path('books/', views.book_list_create, name='book-list-create'),                      # GET, POST
    path('books/<int:pk>/', views.book_detail_update_delete, name='book-detail'),         # GET, PUT, DELETE

    # Author
    path('authors/', views.author_list_create, name='author-list-create'),                # GET, POST

    # Genre
    path('genres/', views.genre_list_create, name='genre-list-create'),                   # GET, POST

    # Borrow Requests
    path('borrow/', views.borrow_request_list_create, name='borrow-request'),              # GET, POST
    path('borrow/<int:pk>/approve/', views.approve_borrow_request, name='borrow-approve'),
    path('borrow/<int:pk>/reject/', views.reject_borrow_request, name='borrow-reject'),
    path('borrow/<int:pk>/return/', views.return_book, name='borrow-return'),

    # Reviews
    path('books/<int:book_id>/reviews/', views.book_reviews, name='book-reviews'),        # GET, POST
]
