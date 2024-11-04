import logging

from fastapi import APIRouter, Depends, HTTPException

from ..dependencies.user import get_logged_in_user
from ..services.login import LoginService
from ..models.payloads.registry import RegistryPayload

router = APIRouter(tags=["Login API"])


@router.post("/registry")
async def registry_user(payload: RegistryPayload) -> str:
    logging.info("Registring user")
    service = LoginService()
    return await service.registry_user(payload.name, payload.password)


@router.post("/login")
async def login(payload: RegistryPayload) -> dict:
    logging.info("Login user")
    service = LoginService()
    return await service.login_user(payload.name, payload.password)


@router.get("/user/{user_name}")
async def get_user_info(user_name: str, logged_in_user: str = Depends(get_logged_in_user)) -> dict:
    print("logged user", logged_in_user)
    logging.info("Get user info")
    service = LoginService()
    if logged_in_user != user_name:
        raise HTTPException(status_code=403, detail="Access denied")
    user_data = await service.get_user_info(user_name)
    print(user_data)
    return {
        "name": user_data[0][1],
        "password": user_data[0][2]
    }