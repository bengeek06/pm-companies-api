"""
schemas.py
----------

This module defines Marshmallow schemas for serializing and validating
the application's data models.
"""

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import ValidationError, validates

from .models import Company
from .logger import logger


class CompanySchema(SQLAlchemyAutoSchema):
    """
    Serialization and validation schema for the Company model.

    This schema is used to serialize and validate Company objects,
    ensuring that all fields conform to the expected format and constraints.
    """
    class Meta:
        """
        Meta options for the Company schema.

        Attributes:
            model (db.Model): The SQLAlchemy model associated with this schema.
            load_instance (bool): Whether to load model instances.
            include_fk (bool): Whether to include foreign keys.
            dump_only (tuple): Fields that are only used for serialization.
        """
        model = Company
        load_instance = True
        include_fk = True
        dump_only = ('id', 'created_at', 'updated_at')

    @validates('name')
    def validate_name(self, value, **kwargs):
        """
        Validate that the name is not empty, unique, and does not exceed 100
        characters.

        Args:
            value (str): The name to validate.

        Raises:
            ValidationError: If the name is empty, already exists, or exceeds
            100 characters.

        Returns:
            str: The validated name.
        """
        _ = kwargs

        if not value:
            logger.error("Validation error: Name cannot be empty.")
            raise ValidationError("Name cannot be empty.")
        company = Company.get_by_name(value)
        if company:
            logger.error("Validation error: Name %s already exists.", value)
            raise ValidationError("Name must be unique.")
        if len(value) > 100:
            logger.error("Validation error: Name exceeds 100 characters.")
            raise ValidationError("Name cannot exceed 100 characters.")
        return value

    @validates('description')
    def validate_description(self, value, **kwargs):
        """
        Validate that the description does not exceed 500 characters.

        Args:
            value (str): The description to validate.

        Raises:
            ValidationError: If the description exceeds 500 characters.

        Returns:
            str: The validated description.
        """
        _ = kwargs
        if value and len(value) > 500:
            logger.error(
                "Validation error: Description exceeds 500 characters."
            )
            raise ValidationError("Description cannot exceed 500 characters.")
        return value

    @validates('logo_url')
    def validate_logo_url(self, value, **kwargs):
        """
        Validate that the logo URL is a valid URL and does not exceed 255
        characters.

        Args:
            value (str): The logo URL to validate.

        Raises:
            ValidationError: If the logo URL is not a valid URL or exceeds 255
            characters.

        Returns:
            str: The validated logo URL.
        """
        _ = kwargs
        if value and not value.startswith(('http://', 'https://')):
            logger.error("Validation error: Logo URL must be a valid URL.")
            raise ValidationError("Logo URL must be a valid URL.")
        if value and len(value) > 255:
            logger.error("Validation error: Logo URL exceeds 255 characters.")
            raise ValidationError("Logo URL cannot exceed 255 characters.")

        return value

    @validates('parent_id')
    def validate_parent_id(self, value, **kwargs):
        """
        Validate that the parent ID is a valid string and exists in the
        database.

        Args:
            value (str): The parent ID to validate.

        Raises:
            ValidationError: If the parent ID is not a string or does not
            exist.

        Returns:
            str: The validated parent ID.
        """
        _ = kwargs
        if value:
            if not isinstance(value, str):
                logger.error(
                    "Validation error: Parent ID must be a valid id or None."
                )
                raise ValidationError(
                    "Parent ID must be a valid string or None."
                )
            parent = Company.get_by_id(value)
            if parent is None:
                logger.error(
                    "Validation error: Parent ID %s does not exist.",
                    value
                )
                raise ValidationError("Parent company does not exist.")
        return value

    @validates('address')
    def validate_address(self, value, **kwargs):
        """
        Validate that the address does not exceed 255 characters.

        Args:
            value (str): The address to validate.

        Raises:
            ValidationError: If the address exceeds 255 characters.

        Returns:
            str: The validated address.
        """
        _ = kwargs
        if value and len(value) > 255:
            logger.error("Validation error: Address exceeds 255 characters.")
            raise ValidationError("Address cannot exceed 255 characters.")
        return value

    @validates('email')
    def validate_email(self, value, **kwargs):
        """
        Validate that the email is a valid email format and does not exceed 100
        characters.

        Args:
            value (str): The email to validate.

        Raises:
            ValidationError: If the email is not a valid format or exceeds 100
            characters.

        Returns:
            str: The validated email.
        """
        _ = kwargs
        if value and len(value) > 100:
            logger.error("Validation error: Email exceeds 100 characters.")
            raise ValidationError("Email cannot exceed 100 characters.")
        if value and '@' not in value:
            logger.error(
                "Validation error: Email must be a valid email address."
            )
            raise ValidationError("Email must be a valid email address.")
        return value

    @validates('phone_number')
    def validate_phone_number(self, value, **kwargs):
        """
        Validate that the phone number does not exceed 20 characters.

        Args:
            value (str): The phone number to validate.

        Raises:
            ValidationError: If the phone number exceeds 20 characters.

        Returns:
            str: The validated phone number.
        """
        _ = kwargs
        if value and len(value) > 20:
            logger.error(
                "Validation error: Phone number exceeds 20 characters."
            )
            raise ValidationError("Phone number cannot exceed 20 characters.")
        return value

    @validates('website')
    def validate_website(self, value, **kwargs):
        """
        Validate that the website is a valid URL and does not exceed 100
        characters.

        Args:
            value (str): The website to validate.

        Raises:
            ValidationError: If the website is not a valid URL or exceeds 100
            characters.

        Returns:
            str: The validated website.
        """
        _ = kwargs
        if value and not value.startswith(('http://', 'https://')):
            logger.error("Validation error: Website must be a valid URL.")
            raise ValidationError("Website must be a valid URL.")
        if value and len(value) > 100:
            logger.error("Validation error: Website exceeds 100 characters.")
            raise ValidationError("Website cannot exceed 100 characters.")
        return value

    @validates('registration_number')
    def validate_registration_number(self, value, **kwargs):
        """
        Validate that the registration number does not exceed 100 characters.

        Args:
            value (str): The registration number to validate.

        Raises:
            ValidationError: If the registration number exceeds 100 characters.

        Returns:
            str: The validated registration number.
        """
        _ = kwargs
        if value and len(value) > 100:
            logger.error(
                "Validation error: Registration number exceeds 100 characters."
            )
            raise ValidationError(
                "Registration number cannot exceed 100 characters."
            )
        return value

    @validates('tax_id')
    def validate_tax_id(self, value, **kwargs):
        """
        Validate that the tax ID does not exceed 50 characters.

        Args:
            value (str): The tax ID to validate.

        Raises:
            ValidationError: If the tax ID exceeds 50 characters.

        Returns:
            str: The validated tax ID.
        """
        _ = kwargs
        if value and len(value) > 50:
            logger.error("Validation error: Tax ID exceeds 50 characters.")
            raise ValidationError("Tax ID cannot exceed 50 characters.")
        return value

    @validates('country')
    def validate_country(self, value, **kwargs):
        """
        Validate that the country does not exceed 100 characters.

        Args:
            value (str): The country to validate.

        Raises:
            ValidationError: If the country exceeds 100 characters.

        Returns:
            str: The validated country.
        """
        _ = kwargs
        if value and len(value) > 100:
            logger.error("Validation error: Country exceeds 100 characters.")
            raise ValidationError("Country cannot exceed 100 characters.")
        return value

    @validates('city')
    def validate_city(self, value, **kwargs):
        """
        Validate that the city does not exceed 100 characters.

        Args:
            value (str): The city to validate.

        Raises:
            ValidationError: If the city exceeds 100 characters.

        Returns:
            str: The validated city.
        """
        _ = kwargs
        if value and len(value) > 100:
            logger.error("Validation error: City exceeds 100 characters.")
            raise ValidationError("City cannot exceed 100 characters.")
        return value

    @validates('postal_code')
    def validate_postal_code(self, value, **kwargs):
        """
        Validate that the postal code does not exceed 20 characters.

        Args:
            value (str): The postal code to validate.

        Raises:
            ValidationError: If the postal code exceeds 20 characters.

        Returns:
            str: The validated postal code.
        """
        _ = kwargs
        if value and len(value) > 20:
            logger.error(
                "Validation error: Postal code exceeds 20 characters."
            )
            raise ValidationError("Postal code cannot exceed 20 characters.")
        return value

    @validates('employees_count')
    def validate_employees_count(self, value, **kwargs):
        """
        Validate that the employees count is a non-negative integer.

        Args:
            value (int): The employees count to validate.

        Raises:
            ValidationError: If the employees count is not a non-negative
            integer.

        Returns:
            int: The validated employees count.
        """
        _ = kwargs
        if value is not None and (not isinstance(value, int) or value < 0):
            logger.error(
                "Validation error: Employees count must be positive integer."
            )
            raise ValidationError(
                "Employees count must be a non-negative integer."
            )
        return value
