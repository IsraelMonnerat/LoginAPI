from jose import jwt
from datetime import datetime, timedelta, timezone


SECRET_KEY = "12345678"
JWT_ALGORITHM = "HS512"


async def criar_token_jwt(name: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(hours=2)
    to_encode = {"exp": expire, "sub": name}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt
