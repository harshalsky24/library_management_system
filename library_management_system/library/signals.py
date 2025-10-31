# app/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import BorrowRequest, Book

@receiver(post_save, sender=BorrowRequest)
def update_book_copies(sender, instance, created, **kwargs):
    book = instance.book

    # If approved → decrease available copies
    if instance.status == "APPROVED":
        if book.available_copies > 0:
            book.available_copies -= 1
            book.save()

    # If returned → increase available copies
    if instance.status == "RETURNED":
        book.available_copies += 1
        book.save()
