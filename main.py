from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from typing import List
import models
import auth

app = FastAPI(title="Login and Signup API")

# In-memory user storage (replace with database in production)
users_db = []

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/signup", response_model=models.User)
def signup(user: models.UserCreate):
    # Check if user already exists
    for db_user in users_db:
        if db_user.email == user.email or db_user.username == user.username:
            raise HTTPException(status_code=400, detail="User already exists")
    
    # Hash the password
    hashed_password = auth.get_password_hash(user.password)
    
    # Create new user
    new_user = models.User(
        id=len(users_db) + 1,
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    
    users_db.append(new_user)
    return new_user

@app.post("/login", response_model=models.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = None
    for db_user in users_db:
        if db_user.username == form_data.username:
            user = db_user
            break
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not auth.verify_password(form_data.password, user.hashed_password):
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

@app.get("/users/me", response_model=models.User)
def read_users_me(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = auth.verify_token(token, credentials_exception)
    
    user = None
    for db_user in users_db:
        if db_user.username == token_data.username:
            user = db_user
            break
    
    if user is None:
        raise credentials_exception
    return user

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
