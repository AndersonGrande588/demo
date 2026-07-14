from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from app.database import get_db
from app.config import get_settings
from app.schemas.usuario import LoginRequest, Token, UsuarioCreate, UsuarioResponse
from app.services.auth_service import authenticate_user, create_user
from app.utils.security import create_access_token

router = APIRouter(prefix="/api/auth", tags=["Autenticacion"])
settings = get_settings()

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contrasena incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "usuario": user
    }

@router.post("/register", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def register(user: UsuarioCreate, db: Session = Depends(get_db)):
    return create_user(db, user)