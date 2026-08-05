
"""
Schemas Initialization Module.

This file serves as the public API entry point for the customer schemas.
It hoists specific Pydantic models from internal modules to the package level,
simplifying import paths for external consumers.

Exposed Schemas:
    - CustomerRegistrationSchema: Handles user sign-up data validation.
    - CustomerPreferencesSchema: Manages user-specific settings and preferences.
    - ApiResponse: Standardized structure for application responses.
    - RegistrationResponseData: Payload structure for successful registration.

Usage:
    Instead of importing from the specific file:
    >>> from app.schemas.customer_schema import CustomerRegistrationSchema

    Import directly from the package:
    >>> from app.schemas import CustomerRegistrationSchema
"""


from app.schemas.customer_schema import (
    CustomerRegistrationSchema, 
    ApiResponse, 
    RegistrationResponseData
)
from app.schemas.preference_schema import CustomerPreferencesSchema
from app.schemas.error_schema import ErrorResponseSchema, ErrorDetail

__all__ = ["CustomerRegistrationSchema", "CustomerPreferencesSchema", "ApiResponse", "RegistrationResponseData", "ErrorResponseSchema", "ErrorDetail"]