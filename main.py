# main.py (Final and Complete Version)
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from datetime import timedelta

# Import everything from our new and updated files
import auth
import models
import schemas
from database import SessionLocal, engine

# This creates the database tables for all models (User and TaskItem)
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# --- Security & Dependencies ---

# This tells FastAPI where the client can go to get a token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency to get the current user from a token
def get_current_active_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decode the token to get the username
        payload = auth.jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except auth.JWTError:
        raise credentials_exception
    
    # Get the user from the database
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None or not user.is_active:
        raise credentials_exception
    return user


# --- Authentication Endpoints ---

@app.post("/users/", response_model=schemas.User, tags=["Authentication"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/token", tags=["Authentication"])
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# --- Secured Endpoints ---

@app.get("/users/me/", response_model=schemas.User, tags=["Secured Endpoints"])
def read_users_me(current_user: models.User = Depends(get_current_active_user)):
    return current_user

@app.post("/tasks/", response_model=schemas.Task, tags=["Secured Endpoints"])
def create_task_for_user(task: schemas.TaskCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    db_task = models.TaskItem(**task.dict(), owner_id=current_user.id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.get("/tasks/", response_model=List[schemas.Task], tags=["Secured Endpoints"])
def read_user_tasks(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    tasks = db.query(models.TaskItem).filter(models.TaskItem.owner_id == current_user.id).all()
    return tasks