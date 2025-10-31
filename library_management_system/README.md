Library Management System — REST API (Django + DRF)

A simple Library Management System API built using Django REST Framework with JWT Authentication.
This system allows students and librarians to manage books, authors, genres, borrow requests, and reviews.

**** Tech Stack

Python 3
Django
Django REST Framework
Simple JWT
SQLite 
drf-yasg (Swagger UI Docs)

#Project Setup Instructions
1) Clone the Repository
git clone <your_repo_url>
cd library_management_system

2) Create Virtual Environment
python -m venv venv

3) Activate Virtual Environment

Windows:

venv\Scripts\activate


4) Install Dependencies
pip install -r requirements.txt

5) Apply Migrations
python manage.py migrate

6) Run Server
python manage.py runserver

**** JWT Authentication Endpoints
Method	Endpoint	Description
POST	/api/register/	Register new user
POST	/api/token/	Get access & refresh token
POST	/api/token/refresh/	Refresh token
**** Book Operations
Method	Endpoint	Role	Description
GET	/api/books/	All	List Books
POST	/api/books/	Librarian	Add Book
GET	/api/books/<id>/	All	Book Details
PUT	/api/books/<id>/	Librarian	Update Book
DELETE	/api/books/<id>/	Librarian	Delete Book
**** Borrow Request Operations
Method	Endpoint	Role	Description
POST	/api/borrow/	Student	Create Borrow Request
GET	/api/borrow/	Student	List My Requests
PATCH	/api/borrow/<id>/approve/	Librarian	Approve Request
PATCH	/api/borrow/<id>/reject/	Librarian	Reject Request
PATCH	/api/borrow/<id>/return/	Student/Librarian	Return Book
**** Book Reviews
Method	Endpoint	Description
POST	/api/books/<id>/reviews/	Add Review
GET	/api/books/<id>/reviews/	View Reviews

**** Swagger UI (API Docs)

After running the project, visit:
http://127.0.0.1:8000/swagger/
 License

This project is open-source and free to use.
