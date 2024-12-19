from flask import Blueprint, request, jsonify
from app.models import db, Book, Member
from app.auth import token_required,generate_token

routes = Blueprint('routes', __name__)

# CRUD for Books
@routes.route('/books', methods=['POST'])
@token_required
def create_book():
    data = request.json

    existing_book = Book.query.filter_by(isbn=data.get('isbn')).first()
    if existing_book:
        return jsonify({"error": "A book with this ISBN already exists"}), 400

    book = Book(
        title=data['title'],
        author=data['author'],
        published_year=data.get('published_year'),
        isbn=data.get('isbn'),
    )
    db.session.add(book)
    db.session.commit()
    return jsonify({"message": "Book created successfully", "book": data}), 201

@routes.route('/get_books', methods=['GET'])
@token_required
def get_books():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    books_query = Book.query
    books = books_query.offset((page - 1) * per_page).limit(per_page).all()
    result = [{"id": b.id, "title": b.title, "author": b.author} for b in books]
    return jsonify(result)

@routes.route('/books/<int:book_id>', methods=['GET'])
@token_required
def get_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    return jsonify({"id": book.id, "title": book.title, "author": book.author})

@routes.route('/books/<int:book_id>', methods=['PUT'])
@token_required
def update_book(book_id):
    data = request.json
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    book.published_year = data.get('published_year', book.published_year)
    db.session.commit()
    return jsonify({"message": "Book updated successfully"})

@routes.route('/books/<int:book_id>', methods=['DELETE'])
@token_required
def delete_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted successfully"})

@routes.route('/books/search', methods=['GET'])
@token_required
def search_books():
    query = request.args.get('query', '')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    books_query = Book.query.filter((Book.title.ilike(f"%{query}%")) | (Book.author.ilike(f"%{query}%")))
    books = books_query.offset((page - 1) * per_page).limit(per_page).all()
    result = [{"id": b.id, "title": b.title, "author": b.author} for b in books]
    return jsonify(result)

@routes.route('/auth/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if username == "admin" and password == "password":
        token = generate_token(user_id=1)  
        return jsonify({"token": token}), 200
    return jsonify({"error": "Invalid credentials"}), 401