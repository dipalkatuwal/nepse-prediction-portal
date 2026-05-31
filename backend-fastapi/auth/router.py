from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.database import get_db
from auth.models import User
from auth.schemas import (
    UserRegisterRequest,
    UserResponse,
    TokenResponse,
    TokenRefreshRequest,
    TokenRefreshResponse,
    LoginRequest,
)
from auth.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
    get_current_user,
)

router = APIRouter(tags=["auth"])


# POST /api/v1/register/  →  replaces accounts.RegisterView
@router.post("/register/", response_model=UserResponse, status_code=201)
def register(payload: UserRegisterRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == payload.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        username=payload.username,
        email=payload.email,
        hashed_password=hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# POST /api/v1/token/  →  replaces simplejwt TokenObtainPairView
@router.post("/token/", response_model=TokenResponse)
def obtain_token(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == payload.username).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return TokenResponse(
        access=create_access_token(user.id),
        refresh=create_refresh_token(user.id),
    )


# POST /api/v1/token/refresh/  →  replaces simplejwt TokenRefreshView
@router.post("/token/refresh/", response_model=TokenRefreshResponse)
def refresh_token(payload: TokenRefreshRequest):
    data = decode_token(payload.refresh)
    if data.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Not a refresh token")
    return TokenRefreshResponse(access=create_access_token(int(data["sub"])))


# GET /api/v1/protected-view/  →  replaces accounts.ProtectedView
@router.get("/protected-view/")
def protected_view(current_user: User = Depends(get_current_user)):
    return {"status": "Request was permitted"}
