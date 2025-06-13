"""
resources.py
-----------
This module defines the resources for managing dummy items in the application.
It includes endpoints for creating, retrieving, updating, and deleting dummy.
"""
from flask import request
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from flask_restful import Resource

from app.models import db, Company
from app.schemas import CompanySchema
from app.logger import logger


company_schema = CompanySchema(session=db.session)
company_schemas = CompanySchema(session=db.session, many=True)


class CompanyListResource(Resource):
    """
    Resource for managing the collection of Companies.

    Methods:
        get():
            Retrieve all companies items from the database.

        post():
            Create a new company item with the provided data.
    """

    def get(self):
        """
        Retrieve all companies items.

        Returns:
            tuple: A tuple containing a list of serialized companies items and
            the HTTP status code 200.
        """
        logger.info("Retrieving all companies items")

        companies = Company.get_all()
        return company_schemas.dump(companies), 200

    def post(self):
        """
        Create a new company item.

        Expects:
            JSON payload with at least the 'name' field.

        Returns:
            tuple: The serialized created company item and HTTP status code 201
                   on success.
            tuple: Error message and HTTP status code 400 or 500 on failure.
        """
        logger.info("Creating a new company item")

        json_data = request.get_json()
        try:
            company_schema.load(json_data)
        except ValidationError as err:
            logger.error("Validation error: %s", err.messages)
            return {"message": "Validation error", "errors": err.messages}, 400

        try:
            company = Company.create(
                name=json_data['name'],
                description=json_data.get('description'),
                address=json_data.get('address'),
                phone_number=json_data.get('phone_number'),
                email=json_data.get('email'),
                website=json_data.get('website'),
                logo_url=json_data.get('logo_url'),
                registration_number=json_data.get('registration_number'),
                tax_id=json_data.get('tax_id'),
                country=json_data.get('country'),
                city=json_data.get('city'),
                postal_code=json_data.get('postal_code'),
                employees_count=json_data.get('employees_count', 0)
            )
        except IntegrityError as e:
            db.session.rollback()
            logger.error("Integrity error: %s", str(e))
            return {"message": "Integrity error", "error": str(e)}, 400
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error("Database error: %s", str(e))
            return {"message": "Database error", "error": str(e)}, 500

        return company_schema.dump(company), 201


class CompanyResource(Resource):
    """
    Resource for managing a single company item by its ID.

    Methods:
        get(company_id):
            Retrieve a company item by its ID.

        put(company_id):
            Update a company item by replacing all fields.

        patch(company_id):
            Partially update a company item.

        delete(company_id):
            Delete a company item by its ID.
    """

    def get(self, company_id):
        """
        Retrieve a company item by its ID.

        Args:
            company_id (str): The ID of the company item to retrieve.

        Returns:
            tuple: The serialized company item and HTTP status code 200 if
                   found.
            tuple: Error message and HTTP status code 404 if not found.
        """
        logger.info("Retrieving dummy with ID: %s", company_id)

        company = Company.get_by_id(company_id)
        if not company:
            logger.warning("Company with ID %s not found", company_id)
            return {"message": "Company not found"}, 404

        return company_schema.dump(company), 200

    def put(self, company_id):
        """
        Update a company item by replacing all fields.

        Args:
            company_id (str): The ID of the company item to update.

        Expects:
            JSON payload with the new 'name' and optionally 'description'.

        Returns:
            tuple: The serialized updated company item and HTTP status code 200
                   on success.
            tuple: Error message and HTTP status code 400, 404, or 500 on
                   failure.
        """
        logger.info("Updating company with ID: %s", company_id)

        json_data = request.get_json()
        try:
            company_schema.load(json_data)
        except ValidationError as err:
            logger.error("Validation error: %s", err.messages)
            return {"message": "Validation error", "errors": err.messages}, 400

        company = Company.get_by_id(company_id)
        if not company:
            logger.warning("Company with ID %s not found", company_id)
            return {"message": "Company not found"}, 404

        try:
            company.update(
                name=json_data['name'],
                description=json_data.get('description'),
                address=json_data.get('address'),
                phone_number=json_data.get('phone_number'),
                email=json_data.get('email'),
                website=json_data.get('website'),
                logo_url=json_data.get('logo_url'),
                registration_number=json_data.get('registration_number'),
                tax_id=json_data.get('tax_id'),
                country=json_data.get('country'),
                city=json_data.get('city'),
                postal_code=json_data.get('postal_code'),
                employees_count=json_data.get('employees_count', 0)
            )
        except IntegrityError as e:
            db.session.rollback()
            logger.error("Integrity error: %s", str(e))
            return {"message": "Integrity error", "error": str(e)}, 400
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error("Database error: %s", str(e))
            return {"message": "Database error", "error": str(e)}, 500

        return company_schema.dump(company), 200

    def patch(self, company_id):
        """
        Partially update a company item.

        Args:
            company_id (str): The ID of the company item to update.

        Expects:
            JSON payload with fields to update
            (e.g., 'name' and/or 'description').

        Returns:
            tuple: The serialized updated company item and HTTP status code 200
                   on success.
            tuple: Error message and HTTP status code 400, 404, or 500 on
                   failure.
        """
        logger.info("Partially updating company with ID: %s", company_id)

        json_data = request.get_json()
        try:
            company_schema.load(json_data, partial=True)
        except ValidationError as err:
            logger.error("Validation error: %s", err.messages)
            return {"message": "Validation error", "errors": err.messages}, 400

        company = Company.get_by_id(company_id)
        if not company:
            logger.warning("Company item with ID %s not found", company_id)
            return {"message": "Company item not found"}, 404

        update_kwargs = {}
        if 'name' in json_data:
            update_kwargs['name'] = json_data['name']
        if 'description' in json_data:
            update_kwargs['description'] = json_data.get('description')
        if 'address' in json_data:
            update_kwargs['address'] = json_data.get('address')
        if 'phone_number' in json_data:
            update_kwargs['phone_number'] = json_data.get('phone_number')
        if 'email' in json_data:
            update_kwargs['email'] = json_data.get('email')
        if 'website' in json_data:
            update_kwargs['website'] = json_data.get('website')
        if 'logo_url' in json_data:
            update_kwargs['logo_url'] = json_data.get('logo_url')
        if 'registration_number' in json_data:
            update_kwargs['registration_number'] = (
                json_data.get('registration_number'))
        if 'tax_id' in json_data:
            update_kwargs['tax_id'] = json_data.get('tax_id')
        if 'country' in json_data:
            update_kwargs['country'] = json_data.get('country')
        if 'city' in json_data:
            update_kwargs['city'] = json_data.get('city')
        if 'postal_code' in json_data:
            update_kwargs['postal_code'] = json_data.get('postal_code')
        if 'employees_count' in json_data:
            update_kwargs['employees_count'] = (
                json_data.get('employees_count', 0))
        if 'is_active' in json_data:
            update_kwargs['is_active'] = json_data.get('is_active', True)
        if 'organization_id' in json_data:
            update_kwargs['organization_id'] = json_data.get('organization_id')
        if 'parent_id' in json_data:
            update_kwargs['parent_id'] = json_data.get('parent_id')

        try:
            company.update(**update_kwargs)
        except IntegrityError as e:
            db.session.rollback()
            logger.error("Integrity error: %s", str(e))
            return {"message": "Integrity error", "error": str(e)}, 400
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error("Database error: %s", str(e))
            return {"message": "Database error", "error": str(e)}, 500

        return company_schema.dump(company), 200

    def delete(self, company_id):
        """
        Delete a company item by its ID.

        Args:
            company_id (str): The ID of the company item to delete.

        Returns:
            tuple: Success message and HTTP status code 204 if deleted.
            tuple: Error message and HTTP status code 404 or 500 on failure.
        """
        logger.info("Deleting company with ID: %s", company_id)

        company = Company.get_by_id(company_id)
        if not company:
            logger.warning("Company with ID %s not found", company_id)
            return {"message": "Company not found"}, 404

        try:
            company.delete()
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error("Database error: %s", str(e))
            return {"message": "Database error", "error": str(e)}, 500

        return {"message": "Company deleted successfully"}, 204
