# test_books.py
import pytest
from app import app, db
from app.models import Book

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_create_book(client):
    response = client.post('/books', json={
        'title': '1984',
        'author': 'George Orwell',
        'published_year': 1949,
        'isbn': '1234567890123'
    })
    assert response.status_code == 201
    assert response.json['title'] == '1984'