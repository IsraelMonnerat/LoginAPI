from abc import ABC, abstractmethod


class DbConnectionHandler(ABC):
    def __init__(self) -> None:
        self.connection = None
    
    @abstractmethod
    async def get_connection(self) -> str: 
        raise NotImplementedError("Should implement get_connection()")
    
    @abstractmethod
    async def close_connection(self):
        raise NotImplementedError("Should implement close_connection()")
