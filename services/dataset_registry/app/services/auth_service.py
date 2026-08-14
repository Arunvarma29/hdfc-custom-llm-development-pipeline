from datetime import UTC, datetime, timedelta

import bcrypt
import jwt
from fastapi import HTTPException
from sqlalchemy.orm import Session

from services.database.app.config import settings
from services.dataset_registry.app.models.user import User


class AuthService:

    def hash_password(
        self,
        password: str,
    ) -> str:
        return bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt(),
        ).decode("utf-8")

    def verify_password(
        self,
        password: str,
        password_hash: str,
    ) -> bool:
        return bcrypt.checkpw(
            password.encode("utf-8"),
            password_hash.encode("utf-8"),
        )

    def create_access_token(
        self,
        user: User,
    ) -> str:
        expires_at = (
            datetime.now(UTC)
            + timedelta(
                minutes=settings.jwt_expire_minutes
            )
        )

        payload = {
            "sub": str(user.id),
            "email": user.email,
            "exp": expires_at,
        }

        return jwt.encode(
            payload,
            settings.jwt_secret_key,
            algorithm=settings.jwt_algorithm,
        )

    def signup(
        self,
        db: Session,
        *,
        full_name: str,
        email: str,
        password: str,
    ):
        normalized_email = (
            email.strip().lower()
        )

        existing_user = (
            db.query(User)
            .filter(
                User.email == normalized_email
            )
            .first()
        )

        if existing_user:
            raise HTTPException(
                status_code=409,
                detail="An account with this email already exists.",
            )

        user = User(
            full_name=full_name.strip(),
            email=normalized_email,
            password_hash=self.hash_password(
                password
            ),
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    def login(
        self,
        db: Session,
        *,
        email: str,
        password: str,
    ):
        normalized_email = (
            email.strip().lower()
        )

        user = (
            db.query(User)
            .filter(
                User.email == normalized_email
            )
            .first()
        )

        if (
            user is None
            or not user.is_active
            or not self.verify_password(
                password,
                user.password_hash,
            )
        ):
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password.",
            )

        token = self.create_access_token(user)

        return {
            "access_token": token,
            "token_type": "bearer",
            "user": user,
        }