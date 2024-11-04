from pydantic import BaseModel


class RegistryPayload(BaseModel):
    name: str
    password: str