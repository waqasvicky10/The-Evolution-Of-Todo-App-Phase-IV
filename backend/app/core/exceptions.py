"""
Custom exception classes for application errors.

This module defines custom exceptions for common error scenarios
that can be handled by FastAPI exception handlers.
"""


class NotFoundError(Exception):
    """
    Raised when a requested resource is not found.

    Used for:
    - Task not found by ID
    - User not found by ID
    - Resource does not exist in database
    """
    pass


class UnauthorizedError(Exception):
    """
    Raised when authentication fails.

    Used for:
    - Invalid credentials (login)
    - Missing authentication token
    - Invalid or expired token
    """
    pass


class ForbiddenError(Exception):
    """
    Raised when user lacks permission to access a resource.

    Used for:
    - User trying to access another user's task
    - User trying to modify another user's data
    - Insufficient permissions
    """
    pass


class ValidationError(Exception):
    """
    Raised when input validation fails.

    Used for:
    - Invalid email format
    - Weak password
    - Description too long/short
    - Required field missing
    """
    pass
