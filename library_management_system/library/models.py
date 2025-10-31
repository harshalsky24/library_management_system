from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    STUDENT = 'STUDENT'
    LIBRARIAN = 'LIBRARIAN'
    ROLE_CHOICES = [(STUDENT, 'Student'), 
                    (LIBRARIAN, 'Librarian')]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)

class Genre(models.Model):
    name = models.CharField(max_length=50)

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    genres = models.ManyToManyField(Genre)
    ISBN = models.CharField(max_length=13)
    available_copies = models.PositiveIntegerField()
    total_copies = models.PositiveIntegerField()

class BorrowRequest(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('RETURNED', 'Returned')
    ]
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    requested_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    returned_at = models.DateTimeField(null=True, blank=True)

class BookReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
