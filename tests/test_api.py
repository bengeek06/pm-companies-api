import json
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.models import Company, db
from app.resources.companies import CompanyListResource


def test_get_companies_empty(client):
    """GET /companies should return an empty list if no companies exist."""
    response = client.get("/companies")
    assert response.status_code == 200
    assert response.json == []

#
# Test for POST /companies endpoint
#
def test_post_company_valid(client):
    """POST /companies with valid data should create a company."""
    data = {
        "name": "Test Company",
        "description": "A test company",
        "email": "test@example.com",
        "employees_count": 10
    }
    response = client.post("/companies", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 201
    assert response.json["name"] == "Test Company"
    assert response.json["description"] == "A test company"
    assert response.json["email"] == "test@example.com"
    assert response.json["employees_count"] == 10

def test_post_company_missing_name(client):
    """POST /companies without a name should fail validation."""
    data = {
        "description": "No name"
    }
    response = client.post("/companies", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 400
    assert "errors" in response.json
    assert "name" in response.json["errors"]

def test_post_company_name_too_long(client):
    """POST /companies with a name > 100 chars should fail validation."""
    data = {
        "name": "A" * 101,
        "description": "Too long name"
    }
    response = client.post("/companies", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 400
    assert "errors" in response.json
    assert "name" in response.json["errors"]

def test_post_company_duplicate_name(client):
    """POST /companies with a duplicate name should fail validation."""
    data = {
        "name": "UniqueName"
    }
    # First insert
    response1 = client.post("/companies", data=json.dumps(data), content_type="application/json")
    assert response1.status_code == 201
    # Duplicate insert
    response2 = client.post("/companies", data=json.dumps(data), content_type="application/json")
    assert response2.status_code == 400
    assert "errors" in response2.json
    assert "name" in response2.json["errors"]

def test_post_company_invalid_email(client):
    """POST /companies with invalid email should fail validation."""
    data = {
        "name": "EmailTest",
        "email": "not-an-email"
    }
    response = client.post("/companies", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 400
    assert "errors" in response.json
    assert "email" in response.json["errors"]

def test_post_company_employees_count_negative(client):
    """POST /companies with negative employees_count should fail validation."""
    data = {
        "name": "NegativeCount",
        "employees_count": -5
    }
    response = client.post("/companies", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 400
    assert "errors" in response.json
    assert "employees_count" in response.json["errors"]

def test_get_companies_with_one(client):
    """GET /companies should return the created company."""
    data = {
        "name": "ListedCompany"
    }
    client.post("/companies", data=json.dumps(data), content_type="application/json")
    response = client.get("/companies")
    assert response.status_code == 200
    assert any(c["name"] == "ListedCompany" for c in response.json)

def test_post_integrity_error(client, monkeypatch):
    """Test that a post raises an IntegrityError."""
    def raise_integrity_error(*args, **kwargs):
        raise IntegrityError("Mocked IntegrityError", None, None)

    # Monkeypatch commit method
    monkeypatch.setattr("app.models.db.session.commit", raise_integrity_error)

    response = client.post(f'/companies', json={'name': 'Dummy'})
    assert response.status_code == 400


def test_post_sqlalchemy_error(client, monkeypatch):
    """Test that a post raises a SQLAlchemyError."""
    def raise_sqlalchemy_error(*args, **kwargs):
        raise SQLAlchemyError("Mocked SQLAlchemyError")

    monkeypatch.setattr("app.models.db.session.commit", raise_sqlalchemy_error)

    response = client.post(f'/companies', json={'name': 'Dummy'})
    assert response.status_code == 500

#
# Test for GET /companies/<id> endpoint
#
def test_get_company_not_found(client):
    """GET /companies/<id> with unknown id should return 404."""
    response = client.get("/companies/unknown-id")
    assert response.status_code == 404
    assert response.json["message"] == "Company not found"

def test_get_company_found(client):
    """GET /companies/<id> should return the company if it exists."""
    # Create a company first
    data = {"name": "FindMe"}
    post_resp = client.post("/companies", data=json.dumps(data), content_type="application/json")
    company_id = post_resp.json["id"]
    response = client.get(f"/companies/{company_id}")
    assert response.status_code == 200
    assert response.json["name"] == "FindMe"

def test_put_company_not_found(client):
    """PUT /companies/<id> with unknown id should return 404."""
    data = {"name": "Updated"}
    response = client.put("/companies/unknown-id", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 404
    assert response.json["message"] == "Company not found"

def test_put_company_invalid(client):
    """PUT /companies/<id> with invalid data should return 400."""
    # Create a company
    data = {"name": "PutTest"}
    post_resp = client.post("/companies", data=json.dumps(data), content_type="application/json")
    company_id = post_resp.json["id"]
    # Now send invalid data (missing name)
    response = client.put(f"/companies/{company_id}", data=json.dumps({}), content_type="application/json")
    assert response.status_code == 400
    assert "errors" in response.json
    assert "name" in response.json["errors"]

def test_put_company_valid(client):
    """PUT /companies/<id> with valid data should update the company."""
    data = {"name": "PutMe"}
    post_resp = client.post("/companies", data=json.dumps(data), content_type="application/json")
    company_id = post_resp.json["id"]
    update = {"name": "PutMeUpdated", "description": "Updated desc"}
    response = client.put(f"/companies/{company_id}", data=json.dumps(update), content_type="application/json")
    assert response.status_code == 200
    assert response.json["name"] == "PutMeUpdated"
    assert response.json["description"] == "Updated desc"

def test_update_integrity_error(client, monkeypatch):
    """Test that a update raises an IntegrityError."""
    def raise_integrity_error(*args, **kwargs):
        raise IntegrityError("Mocked IntegrityError", None, None)

    # First, create an object to update
    company = Company.create(name='Test Dummy', description='A test dummy')

    # Monkeypatch commit method
    monkeypatch.setattr("app.models.db.session.commit", raise_integrity_error)

    response = client.put(f'/companies/{company.id}', json={'name': 'Updated Dummy'})
    assert response.status_code == 400


def test_update_sqlalchemy_error(client, monkeypatch):
    """Test that a update raises a SQLAlchemyError."""
    def raise_sqlalchemy_error(*args, **kwargs):
        raise SQLAlchemyError("Mocked SQLAlchemyError")

    # First, create an object to update
    company = Company.create(name='Test Dummy', description='A test dummy')

    monkeypatch.setattr("app.models.db.session.commit", raise_sqlalchemy_error)

    response = client.put(f'/companies/{company.id}', json={'name': 'Updated Dummy'})
    assert response.status_code == 500


def test_patch_company_not_found(client):
    """PATCH /companies/<id> with unknown id should return 404."""
    response = client.patch("/companies/unknown-id", data=json.dumps({"name": "X"}), content_type="application/json")
    assert response.status_code == 404

def test_patch_company_invalid(client):
    """PATCH /companies/<id> with invalid data should return 400."""
    data = {"name": "PatchTest"}
    post_resp = client.post("/companies", data=json.dumps(data), content_type="application/json")
    company_id = post_resp.json["id"]
    # Invalid: name too long
    response = client.patch(f"/companies/{company_id}", data=json.dumps({"name": "A"*101}), content_type="application/json")
    assert response.status_code == 400
    assert "errors" in response.json
    assert "name" in response.json["errors"]

def test_patch_company_valid(client):
    """PATCH /companies/<id> with valid data should update the company."""
    data = {"name": "PatchMe"}
    post_resp = client.post("/companies", data=json.dumps(data), content_type="application/json")
    company_id = post_resp.json["id"]
    patch = {"description": "Patched desc"}
    response = client.patch(f"/companies/{company_id}", data=json.dumps(patch), content_type="application/json")
    assert response.status_code == 200
    assert response.json["description"] == "Patched desc"

def test_patch_company_all_fields(client):
    """PATCH /companies/<id> should update each field individually."""
    # Create a company
    data = {
        "name": "PatchAll",
        "description": "desc",
        "address": "addr",
        "phone_number": "0123456789",
        "email": "patch@all.com",
        "website": "https://patchall.com",
        "logo_url": "https://patchall.com/logo.png",
        "registration_number": "REG123",
        "tax_id": "TAX123",
        "country": "France",
        "city": "Paris",
        "postal_code": "75000",
        "employees_count": 5,
        "is_active": True,
        "organization_id": "org1",
        "parent_id": None
    }
    post_resp = client.post("/companies", data=json.dumps(data), content_type="application/json")
    company_id = post_resp.json["id"]

    # Patch each field one by one and check the update
    patch_fields = {
        "name": "PatchedName",
        "description": "PatchedDesc",
        "address": "PatchedAddr",
        "phone_number": "0987654321",
        "email": "patched@email.com",
        "website": "https://patched.com",
        "logo_url": "https://patched.com/logo.png",
        "registration_number": "REG999",
        "tax_id": "TAX999",
        "country": "Germany",
        "city": "Berlin",
        "postal_code": "10115",
        "employees_count": 42,
        "is_active": False,
        "organization_id": "org2",
        "parent_id": None
    }

    for field, value in patch_fields.items():
        patch_data = {field: value}
        response = client.patch(f"/companies/{company_id}", data=json.dumps(patch_data), content_type="application/json")
        assert response.status_code == 200
        assert response.json[field] == value

def test_partial_update_integrity_error(client, monkeypatch):
    """Test that a partial update raises an IntegrityError."""
    def raise_integrity_error(*args, **kwargs):
        raise IntegrityError("Mocked IntegrityError", None, None)

    # First, create an object to update
    company = Company.create(name='Test Dummy', description='A test dummy')

    # Monkeypatch commit method
    monkeypatch.setattr("app.models.db.session.commit", raise_integrity_error)

    response = client.patch(f'/companies/{company.id}', json={'name': 'Updated Dummy'})
    assert response.status_code == 400


def test_partial_update_sqlalchemy_error(client, monkeypatch):
    """Test that a partial update raises a SQLAlchemyError."""
    def raise_sqlalchemy_error(*args, **kwargs):
        raise SQLAlchemyError("Mocked SQLAlchemyError")

    # First, create an object to update
    company = Company.create(name='Test Dummy', description='A test dummy')

    monkeypatch.setattr("app.models.db.session.commit", raise_sqlalchemy_error)

    response = client.patch(f'/companies/{company.id}', json={'name': 'Updated Dummy'})
    assert response.status_code == 500

def test_delete_company_not_found(client):
    """DELETE /companies/<id> with unknown id should return 404."""
    response = client.delete("/companies/unknown-id")
    assert response.status_code == 404
    assert response.json["message"] == "Company not found"

def test_delete_company_success(client):
    """DELETE /companies/<id> should delete the company."""
    data = {"name": "DeleteMe"}
    post_resp = client.post("/companies", data=json.dumps(data), content_type="application/json")
    company_id = post_resp.json["id"]
    response = client.delete(f"/companies/{company_id}")
    assert response.status_code == 204
    # Should not be found anymore
    get_resp = client.get(f"/companies/{company_id}")
    assert get_resp.status_code == 404

def test_delete_sqlalchemy_error(client, monkeypatch):
    """DELETE /companies/<id> should handle SQLAlchemy errors gracefully."""
    def raise_sqlalchemy_error(*args, **kwargs):
        raise SQLAlchemyError("Mocked SQLAlchemyError")

    # First, create a dummy object to delete
    company = Company.create(name='Test Dummy', description='A test dummy')

    monkeypatch.setattr("app.models.db.session.commit", raise_sqlalchemy_error)

    response = client.delete(f'/companies/{company.id}')
    assert response.status_code == 500
    data = json.loads(response.data)
    assert 'message' in data
    assert 'error' in data
    assert data['message'] == 'Database error'
