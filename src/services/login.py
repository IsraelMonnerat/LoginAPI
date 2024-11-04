from typing import Tuple
from ..infra.login_db.login_repository import ResumeConnectionHandler


class LoginService:
    def __init__(self) -> None:
        self.repository = ResumeConnectionHandler()
    

    async def registry_user(self, name: str, password: str) -> str:
        await self.repository()
        await self.repository.registry_user(name, password)
        return "User registered successfully"


    async def login_user(self, name: str, password: str) -> Tuple[bool, str]:
        await self.repository()
        return await self.repository.login_user(name, password)
    

    async def get_user_info(self, name: str) -> Tuple[bool, str]:
        await self.repository()
        return await self.repository.get_filtered_value("name", name)