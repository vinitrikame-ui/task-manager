from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")

        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        return username

    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")