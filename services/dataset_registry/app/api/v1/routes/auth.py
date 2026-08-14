from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from services.dataset_registry.app.api.dependencies import (
    get_current_user,
    get_db,
)
from services.dataset_registry.app.models.user import User
from services.dataset_registry.app.schemas.auth import (
    AuthResponse,
    LoginRequest,
    SignupRequest,
    UserResponse,
)
from services.dataset_registry.app.services.auth_service import (
    AuthService,
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

service = AuthService()


@router.post(
    "/signup",
    response_model=UserResponse,
    status_code=201,
)
def signup(
    payload: SignupRequest,
    db: Session = Depends(get_db),
):
    return service.signup(
        db=db,
        full_name=payload.full_name,
        email=payload.email,
        password=payload.password,
    )


@router.post(
    "/login",
    response_model=AuthResponse,
)
def login(
    payload: LoginRequest,
    db: Session = Depends(get_db),
):
    return service.login(
        db=db,
        email=payload.email,
        password=payload.password,
    )


@router.get(
    "/me",
    response_model=UserResponse,
)
def get_me(
    current_user: User = Depends(
        get_current_user
    ),
):
    return current_user