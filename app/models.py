"""
models.py
---------

This module defines the SQLAlchemy database models for the application.
It includes the Company model, representing a business entity with hierarchical
organization, and provides utility methods for database record management.
"""
import uuid
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Company(db.Model):
    """
    Data model for a Company entity.

    This model represents a company, including its general information,
    hierarchical relationships (parent_id), organization association,
    and provides CRUD (Create, Read, Update, Delete) utility methods.
    """

    __tablename__ = 'companies'

    id = db.Column(db.String(40), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    logo_url = db.Column(db.String(255), nullable=True)
    parent_id = db.Column(
        db.String(100),
        db.ForeignKey('companies.id'),
        nullable=True
    )
    organization_id = db.Column(db.String(100), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    phone_number = db.Column(db.String(20), nullable=True)
    website = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    is_active = db.Column(db.Boolean, default=True)
    registration_number = db.Column(db.String(100), nullable=True)
    tax_id = db.Column(db.String(50), nullable=True)
    country = db.Column(db.String(100), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    postal_code = db.Column(db.String(20), nullable=True)
    employees_count = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        """
        Returns a string representation of the Company object.
        """
        return (
            f"<Company {self.name}> ("
            f"ID: {self.id}, "
            f"Description: {self.description}, "
            f"Logo URL: {self.logo_url}, "
            f"Parent ID: {self.parent_id}, "
            f"Organization ID: {self.organization_id}, "
            f"Address: {self.address}, "
            f"Email: {self.email}, "
            f"Phone Number: {self.phone_number}, "
            f"Website: {self.website}, "
            f"Created At: {self.created_at}, "
            f"Updated At: {self.updated_at}, "
            f"Is Active: {self.is_active}, "
            f"Registration Number: {self.registration_number}, "
            f"Tax ID: {self.tax_id}, "
            f"Country: {self.country}, "
            f"City: {self.city}, "
            f"Postal Code: {self.postal_code}, "
            f"Employees Count: {self.employees_count}"
            f")"
        )

    @classmethod
    def get_all(cls):
        """
        Retrieve all Company records from the database.

        Returns:
            list: List of all Company objects.
        """
        return cls.query.all()

    @classmethod
    def get_by_id(cls, company_id):
        """
        Retrieve a Company record by its ID.

        Args:
            company_id (str): The unique identifier of the company.

        Returns:
            Company: The Company object if found, else None.
        """
        return cls.query.get(company_id)

    @classmethod
    def get_by_name(cls, name):
        """
        Retrieve a Company record by its name.

        Args:
            name (str): The name of the company.

        Returns:
            Company: The Company object if found, else None.
        """
        return cls.query.filter_by(name=name).first()

    @classmethod
    def create(cls,
               name,
               description=None,
               logo_url=None,
               parent_id=None,
               address=None,
               email=None,
               phone_number=None,
               website=None,
               registration_number=None,
               tax_id=None,
               country=None,
               city=None,
               postal_code=None,
               is_active=True,
               employees_count=None,
               ):
        """
        Create a new Company record and add it to the database.

        Args:
            name (str): Name of the company.
            description (str, optional): Description of the company.
            logo_url (str, optional): Logo URL.
            parent_id (str, optional): Parent company ID.
            address (str, optional): Company address.
            email (str, optional): Contact email.
            phone_number (str, optional): Contact phone number.
            website (str, optional): Website URL.
            registration_number (str, optional): Registration number.
            tax_id (str, optional): Tax identifier.
            country (str, optional): Country.
            city (str, optional): City.
            postal_code (str, optional): Postal code.
            is_active (bool, optional): Active status of the company.
            employees_count (int, optional): Number of employees.

        Returns:
            Company: The created Company object.
        """
        company_id = str(uuid.uuid4())
        company = cls(
            id=company_id,
            name=name,
            description=description,
            logo_url=logo_url,
            parent_id=parent_id,
            address=address,
            email=email,
            phone_number=phone_number,
            website=website,
            registration_number=registration_number,
            tax_id=tax_id,
            country=country,
            city=city,
            is_active=is_active,
            employees_count=employees_count,
            organization_id=None,
            postal_code=postal_code,
            created_at=db.func.now(),
            updated_at=db.func.now()
            )
        db.session.add(company)
        db.session.commit()
        return company

    def update(
        self,
        name=None,
        description=None,
        logo_url=None,
        parent_id=None,
        organization_id=None,
        address=None,
        email=None,
        phone_number=None,
        website=None,
        registration_number=None,
        tax_id=None,
        country=None,
        city=None,
        postal_code=None,
        employees_count=None,
        is_active=None
    ):
        """
        Update the attributes of the Company entity and save changes.

        Args:
            name (str, optional): New name.
            description (str, optional): New description.
            logo_url (str, optional): New logo URL.
            parent_id (str, optional): New parent company ID.
            organization_id (str, optional): New organization ID.
            address (str, optional): New address.
            email (str, optional): New email.
            phone_number (str, optional): New phone number.
            website (str, optional): New website.
            registration_number (str, optional): New registration number.
            tax_id (str, optional): New tax ID.
            country (str, optional): New country.
            city (str, optional): New city.
            postal_code (str, optional): New postal code.
            employees_count (int, optional): New number of employees.
            is_active (bool, optional): Active status.
        """
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        if logo_url is not None:
            self.logo_url = logo_url
        if parent_id is not None:
            self.parent_id = parent_id
        if organization_id is not None:
            self.organization_id = organization_id
        if address is not None:
            self.address = address
        if email is not None:
            self.email = email
        if phone_number is not None:
            self.phone_number = phone_number
        if website is not None:
            self.website = website
        if registration_number is not None:
            self.registration_number = registration_number
        if tax_id is not None:
            self.tax_id = tax_id
        if country is not None:
            self.country = country
        if city is not None:
            self.city = city
        if postal_code is not None:
            self.postal_code = postal_code
        if employees_count is not None:
            self.employees_count = employees_count
        if is_active is not None:
            self.is_active = is_active

        self.updated_at = db.func.now()
        db.session.commit()

    def delete(self):
        """
        Delete the Company record from the database.
        """
        db.session.delete(self)
        db.session.commit()
