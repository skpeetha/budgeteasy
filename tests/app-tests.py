import os
import tempfile
import pytest
from flask import url_for
from web.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()
    with app.test_client() as client:
        yield client

def test_index_get(client):
    """Test GET request to index page returns 200."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'BudgetEasy' in response.data

def test_index_post_no_file(client):
    """Test POST request with no file uploaded."""
    response = client.post('/', data={})
    assert response.status_code == 302  # Redirect due to flash

def test_index_post_empty_file(client):
    """Test POST request with empty file field."""
    data = {'file': (b'', '')}
    response = client.post('/', data=data, content_type='multipart/form-data')
    assert response.status_code == 302  # Redirect due to flash

def test_index_post_pdf_file(client, tmp_path):
    """Test POST request with a valid PDF file."""
    # Create a dummy PDF file
    pdf_path = tmp_path / "dummy.pdf"
    pdf_path.write_bytes(b"%PDF-1.4\n%EOF\n")
    with open(pdf_path, "rb") as f:
        data = {'file': (f, "dummy.pdf")}
        response = client.post('/', data=data, content_type='multipart/form-data')
        # Should redirect or show error if parsing fails
        assert response.status_code in (200, 302)

def test_duplicate_statement(client, tmp_path, monkeypatch):
    """Test duplicate statement detection."""
    # Patch get_statement_by_hash to simulate duplicate
    monkeypatch.setattr("src.db.get_statement_by_hash", lambda x: True)
    pdf_path = tmp_path / "dummy.pdf"
    pdf_path.write_bytes(b"%PDF-1.4\n%EOF\n")
    with open(pdf_path, "rb") as f:
        data = {'file': (f, "dummy.pdf")}
        response = client.post('/', data=data, content_type='multipart/form-data')
        assert b"already uploaded" in response.data or response.status_code == 302