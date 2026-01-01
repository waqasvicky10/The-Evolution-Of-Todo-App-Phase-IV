"""
User service for registration and authentication logic.

This module provides business logic for user management operations.
"""

from sqlmodel import Session, select
from fastapi import HTTPException, status
from app.models.user import User
from app.core.security import hash_password, verify_password


def create_user(db: Session, email: str, password: str) -> User:
    """
    Create a new user account.

    Args:
        db: Database session
        email: User email address
        password: Plain text password (will be hashed)

    Returns:
        Created user object

    Raises:
        HTTPException 409: If email already exists
        HTTPException 500: If database error occurs

    Example:
        >>> user = create_user(db, "user@example.com", "SecurePass123!")
        >>> print(user.email)
        user@example.com
    """
    # Check if email already exists
    existing_user = db.exec(select(User).where(User.email == email)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists"
        )

    # Hash password
    hashed_password = hash_password(password)

    # Create user
    user = User(email=email, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def authenticate_user(db: Session, email: str, password: str) -> User:
    """
    Authenticate user by email and password.

    Args:
        db: Database session
        email: User email address
        password: Plain text password

    Returns:
        Authenticated user object

    Raises:
        HTTPException 401: If credentials are invalid (generic message for security)

    Example:
        >>> user = authenticate_user(db, "user@example.com", "SecurePass123!")
        >>> print(user.id)
        1
    """
    # Query user by email
    user = db.exec(select(User).where(User.email == email)).first()

    if not user:
        # Generic error message for security (don't reveal if email exists)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Verify password
    if not verify_password(password, user.hashed_password):
        # Same generic error message
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    return user


def get_user_by_id(db: Session, user_id: int) -> User:
    """
    Get user by ID.

    Args:
        db: Database session
        user_id: User ID

    Returns:
        User object

    Raises:
        HTTPException 404: If user not found

    Example:
        >>> user = get_user_by_id(db, 1)
        >>> print(user.email)
        user@example.com
    """
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user
