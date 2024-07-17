from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models, schemas, crud, auth, database
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/me/", response_model=schemas.User)
def read_users_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    return user

@app.post("/notes", response_model=schemas.Note)
def post_user_note(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
      credentials_exception = HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Could not validate credentials",
      headers={"WWW-Authenticate": "Bearer"},
      )
      try:
          payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
          username: str = payload.get("sub")
          if username is None:
            raise credentials_exception
      except JWTError:
        raise credentials_exception
      user = crud.get_user_by_username(db, username=username)
      if user is None:
        raise credentials_exception
      #logic for grabbing notes in user database
      return crud.create_note(db=db, user=user)
      
@app.get("/notes", response_model=schemas.Note)
def read_user_note(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
      credentials_exception = HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Could not validate credentials",
      headers={"WWW-Authenticate": "Bearer"},
      )
      try:
          payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
          username: str = payload.get("sub")
          if username is None:
            raise credentials_exception
      except JWTError:
        raise credentials_exception
      user = crud.get_user_by_username(db, username=username)
      if user is None:
        raise credentials_exception
      #logic for grabbing notes in user database  
      return user.note
