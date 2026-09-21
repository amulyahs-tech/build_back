import os
import datetime
from typing import Optional
import jwt
try:
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify raw password against bcrypt hash."""
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(password: str) -> str:
        """Generate bcrypt hash for password."""
        return pwd_context.hash(password)

except ImportError:
    try:
        import bcrypt

        def verify_password(plain_password: str, hashed_password: str) -> bool:
            try:
                return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
            except Exception:
                return False

        def get_password_hash(password: str) -> str:
            salt = bcrypt.gensalt()
            return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    except ImportError:
        import hashlib

        def verify_password(plain_password: str, hashed_password: str) -> bool:
            return hashlib.sha256(plain_password.encode('utf-8')).hexdigest() == hashed_password

        def get_password_hash(password: str) -> str:
            return hashlib.sha256(password.encode('utf-8')).hexdigest()

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.models import User
from backend.app.schemas import TokenData

# JWT Configuration
JWT_SECRET = os.getenv("JWT_SECRET", "rebuild-ai-insecure-dev-secret-replace-in-env-32bytes-long")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)



def create_access_token(data: dict, expires_delta: Optional[datetime.timedelta] = None) -> str:
    """Encode user information into signed JWT."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """Decode and validate a JWT access token."""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        return payload
    except (jwt.PyJWTError, Exception):
        return None


def get_current_user(token: Optional[str] = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """FastAPI dependency to extract and authenticate current user from Bearer token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate authentication credentials. Please log in again.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not token:
        raise credentials_exception

    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user


def get_optional_current_user(token: Optional[str] = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Optional[User]:
    """Extract current user if token is provided, without raising 401."""
    if not token:
        return None
    payload = decode_access_token(token)
    if not payload:
        return None
    email = payload.get("sub")
    if not email:
        return None
    return db.query(User).filter(User.email == email).first()


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """Enforce ADMIN role."""
    if current_user.user_type != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access restricted: Administrator privilege required."
        )
    return current_user


def require_seller(current_user: User = Depends(get_current_user)) -> User:
    """Enforce SELLER or BOTH role."""
    if current_user.user_type not in ["SELLER", "BOTH", "ADMIN"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access restricted: Seller registration required."
        )
    return current_user
