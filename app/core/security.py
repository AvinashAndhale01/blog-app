from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
import jwt
from .config import setting


password_hash = PasswordHash.recommended()


DUMMY_HASH = password_hash.hash("dummy")


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password):
    return password_hash.hash(password)


def create_access_token(data: dict, expire_delta: timedelta | None = None):
    to_encode = data.copy
    if expire_delta:
        expire = datetime.now(timezone.utc) + expire_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, setting.secret_key, algorithm=setting.algorithm)
    return encoded_jwt