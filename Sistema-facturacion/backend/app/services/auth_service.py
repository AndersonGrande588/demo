from sqlalchemy.orm import Session
from app.models.usuario import Usuario, RolUsuario
from app.schemas.usuario import UsuarioCreate
from app.utils.security import get_password_hash, verify_password
from fastapi import HTTPException, status

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(Usuario).filter(Usuario.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        return None
    return user

def create_user(db: Session, user: UsuarioCreate):
    existing = db.query(Usuario).filter(Usuario.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="El email ya esta registrado")
    
    db_user = Usuario(
        nombre=user.nombre,
        email=user.email,
        password_hash=get_password_hash(user.password),
        rol=user.rol,
        activo=user.activo
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_id(db: Session, user_id: int):
    return db.query(Usuario).filter(Usuario.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Usuario).offset(skip).limit(limit).all()

def update_user(db: Session, user_id: int, user_data):
    user = db.query(Usuario).filter(Usuario.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    update_data = user_data.dict(exclude_unset=True)
    if "password" in update_data and update_data["password"]:
        update_data["password_hash"] = get_password_hash(update_data.pop("password"))
    
    for field, value in update_data.items():
        setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: int):
    user = db.query(Usuario).filter(Usuario.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    user.activo = False
    db.commit()
    return user

def init_admin_user(db: Session):
    admin = db.query(Usuario).filter(Usuario.email == "admin@hayabuza.com").first()
    if not admin:
        admin = Usuario(
            nombre="Anderson Grande",
            email="admin@hayabuza.com",
            password_hash=get_password_hash("admin123"),
            rol=RolUsuario.ADMINISTRADOR,
            activo=True
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)
    return admin