
from jose import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, ValidationError

from ..infra.login_db.login_repository import ResumeConnectionHandler
from ..infra.security import SECRET_KEY, JWT_ALGORITHM


class TokenPayload(BaseModel):
    sub: str

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl="/login/api/login"
)

async def get_logged_in_user(token: str = Depends(reusable_oauth2)) -> str:
    repository = ResumeConnectionHandler()
    try:
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=[JWT_ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    await repository()
    user = repository.get_filtered_value("name", token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return token_data.sub