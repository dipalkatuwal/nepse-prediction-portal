from pydantic import BaseModel, EmailStr, field_validator


class UserRegisterRequest(BaseModel):
    """Replaces DRF UserSerializer (registration input)."""
    username: str
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def password_min_length(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v


class UserResponse(BaseModel):
    """Replaces DRF UserSerializer (registration output)."""
    id: int
    username: str
    email: str

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    """Replaces simplejwt TokenObtainPairView response."""
    access: str
    refresh: str


class TokenRefreshRequest(BaseModel):
    refresh: str


class TokenRefreshResponse(BaseModel):
    access: str


class LoginRequest(BaseModel):
    username: str
    password: str
