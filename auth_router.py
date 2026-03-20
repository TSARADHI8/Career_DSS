from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import get_db
import models, schemas, auth

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
def register(payload: schemas.UserRegister, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == payload.email).first()
    if existing:
        return JSONResponse(status_code=400, content={"detail": "Email already registered"})
    user = models.User(
        name=payload.name,
        email=payload.email,
        hashed_password=auth.hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return JSONResponse(content={"id": user.id, "name": user.name, "email": user.email, "created_at": str(user.created_at)})


@router.post("/login")
def login(payload: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == payload.email).first()
    if not user or not auth.verify_password(payload.password, user.hashed_password):
        return JSONResponse(status_code=401, content={"detail": "Invalid email or password"})
    token = auth.create_token(user.id)
    return JSONResponse(content={"access_token": token, "token_type": "bearer"})


@router.get("/me")
def me(current_user: models.User = Depends(auth.get_current_user)):
    return JSONResponse(content={"id": current_user.id, "name": current_user.name, "email": current_user.email, "created_at": str(current_user.created_at)})
