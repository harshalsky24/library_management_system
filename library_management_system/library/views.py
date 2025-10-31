from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Book,Author,Genre,BookReview,BorrowRequest
from .serializers import UserSerializer,BookCreateUpdateSerializer,BookSerializer,BorrowRequestSerializer,AuthorSerializer,GenreSerializer,ReviewSerializer
from drf_yasg.utils import swagger_auto_schema

@swagger_auto_schema(
    method='post',
    request_body=UserSerializer,
    responses={201: "User Registered Successfully"}
)
@api_view(['POST'])
@permission_classes([]) 
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'msg': 'User created'}, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET', 'POST'])
def book_list_create(request):
    if request.method == 'GET':
        books = Book.objects.all()
        author = request.GET.get('author')
        genre = request.GET.get('genre')
        if author:
            books = books.filter(author__name__icontains=author)
        if genre:
            books = books.filter(genre__name__icontains=genre)
        return Response(BookSerializer(books, many=True).data)

    if request.user.role != 'LIBRARIAN':
        return Response({'error': 'Only librarians can add books'}, status=403)
    serializer = BookCreateUpdateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
def book_detail_update_delete(request, pk):
    try:
        book = Book.objects.get(id=pk)
    except Book.DoesNotExist:
        return Response({'error': 'Book not found'}, status=404)

    if request.method == 'GET':
        return Response(BookSerializer(book).data)

    if request.user.role != 'LIBRARIAN':
        return Response({'error': 'Only librarians allowed'}, status=403)

    if request.method == 'PUT':
        serializer = BookCreateUpdateSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    if request.method == 'DELETE':
        book.delete()
        return Response({'msg': 'Book deleted'}, status=204)

@api_view(['GET', 'POST'])
def author_list_create(request):
    if request.method == 'GET':
        return Response(AuthorSerializer(Author.objects.all(), many=True).data)
    if request.user.role != 'LIBRARIAN':
        return Response({'error': 'Only librarians can add authors'}, status=403)
    serializer = AuthorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors)

@api_view(['GET', 'POST'])
def genre_list_create(request):
    if request.method == 'GET':
        return Response(GenreSerializer(Genre.objects.all(), many=True).data)
    if request.user.role != 'LIBRARIAN':
        return Response({'error': 'Only librarians can add genres'}, status=403)
    serializer = GenreSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def borrow_request_list_create(request):

    # GET → List only current user's borrow requests
    if request.method == 'GET':
        requests = BorrowRequest.objects.filter(user=request.user)
        serializer = BorrowRequestSerializer(requests, many=True)
        return Response(serializer.data)

    # POST → Create a borrow request (Student Only)
    if request.user.role != 'STUDENT':
        return Response({'error': 'Only students can borrow books'}, status=403)

    # We take book_id from request data
    book_id = request.data.get('book_id')
    if not book_id:
        return Response({'error': 'book_id is required'}, status=400)

    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return Response({'error': 'Book not found'}, status=404)

    # Check book availability
    if book.available_copies <= 0:
        return Response({'error': 'No copies available'}, status=400)

    # Save borrow request (user auto-filled)
    serializer = BorrowRequestSerializer(data={'book': book.id})
    if serializer.is_valid():
        serializer.save(user=request.user, status='PENDING')
        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)



@api_view(['PATCH'])
def approve_borrow_request(request, pk):
    if request.user.role != 'LIBRARIAN':
        return Response({'error': 'Only librarians can approve'}, status=403)
    try:
        req = BorrowRequest.objects.get(id=pk)
        req.status = 'APPROVED'
        req.save()
        return Response({'msg': 'Approved'})
    except:
        return Response({'error': 'Request not found'}, status=404)

@api_view(['PATCH'])
def reject_borrow_request(request, pk):
    if request.user.role != 'LIBRARIAN':
        return Response({'error': 'Only librarians can reject'}, status=403)
    try:
        req = BorrowRequest.objects.get(id=pk)
        req.status = 'REJECTED'
        req.save()
        return Response({'msg': 'Rejected'})
    except:
        return Response({'error': 'Request not found'}, status=404)

@api_view(['PATCH'])
def return_book(request, pk):
    try:
        req = BorrowRequest.objects.get(id=pk)
        req.status = 'RETURNED'
        req.book.available = True
        req.book.save()
        req.save()
        return Response({'msg': 'Book returned'})
    except:
        return Response({'error': 'Request not found'}, status=404)

@api_view(['GET', 'POST'])
def book_reviews(request, book_id):
    if request.method == 'GET':
        reviews = BookReview.objects.filter(book_id=book_id)
        return Response(ReviewSerializer(reviews, many=True).data)

    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user, book_id=book_id)
        return Response(serializer.data, status=201)
    return Response(serializer.errors)
