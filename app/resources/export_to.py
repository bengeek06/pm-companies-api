"""
export.py
---------

This module defines the ExportCSVResource for exporting all Dummy records
from the database as a downloadable CSV file through a REST endpoint.
"""
import io
import csv
from flask_restful import Resource
from flask import make_response
from app.models import Company


class ExportCSVResource(Resource):
    """
    Resource for exporting data to a CSV file.

    Methods:
        get():
            Export data to a CSV file and return it as a response.
    """

    def get(self):
        """
        Export all Company records to a CSV file and return it as a response.

        Returns:
            Response: A CSV file containing all Company records.
        """
        # Retrieve all Company records
        companies = Company.get_all()

        # Prepare CSV in memory
        output = io.StringIO()
        writer = csv.writer(output)
        # Write header with all fields
        writer.writerow([
            "id", "name", "description", "logo_url", "parent_id",
            "organization_id", "address", "email", "phone_number", "website",
            "created_at", "updated_at", "is_active", "registration_number",
            "tax_id", "country", "city", "postal_code", "employees_count"
        ])
        # Write data rows
        for company in companies:
            writer.writerow([
                company.id,
                company.name,
                company.description,
                company.logo_url,
                company.parent_id,
                company.organization_id,
                company.address,
                company.email,
                company.phone_number,
                company.website,
                company.created_at.isoformat() if company.created_at else "",
                company.updated_at.isoformat() if company.updated_at else "",
                company.is_active,
                company.registration_number,
                company.tax_id,
                company.country,
                company.city,
                company.postal_code,
                company.employees_count
            ])

        # Create response
        response = make_response(output.getvalue())
        response.headers['Content-Type'] = 'text/csv'
        response.headers['Content-Disposition'] = (
            'attachment; filename=export.csv')
        return response
