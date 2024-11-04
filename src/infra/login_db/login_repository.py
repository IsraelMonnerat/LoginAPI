import os
import logging
import psycopg2
from typing import List, Tuple
from fastapi import HTTPException

from ..security import criar_token_jwt

from ..db_connection_handler import DbConnectionHandler

class ResumeConnectionHandler(DbConnectionHandler):
    def __init__(self):
        super().__init__()
        self.cursor = None
        self.connection = None

    async def __call__(self):
        await self.get_connection()

    async def get_connection(self) -> None:
        """
        Asynchronously establishes a connection to the database.

        This method attempts to connect to the database using the provided environment variables.
        If a connection cannot be established, an HTTPException with a status code of 500 and
        an error message is raised.

        Parameters:
            self (ResumeConnectionHandler): The instance of the ResumeConnectionHandler class.

        Returns:
            None: This method does not return anything.

        Raises:
            HTTPException: If a connection to the database cannot be established.
        """
        logging.info("Getting connection to database")
        try:
            self.connection = psycopg2.connect(
                host=os.environ.get("DB_HOST", "localhost"),
                database=os.environ.get("POSTGRES_DB"),
                user=os.environ.get("POSTGRES_USER"),
                password=os.environ.get("POSTGRES_PASSWORD"),
                port=os.environ.get("DB_PORT")
            )
        except Exception as error:
            logging.error("Failed to connect to database.  Error: %s", error)           
            raise HTTPException(
                    status_code=500, 
                    detail=f"Failed to connect to database.  Error: {error}") from error

        self.cursor = self.connection.cursor()

    async def close_connection(self) -> None:
        """
        Close the connection to the database.

        This method closes the connection to the database and sets the connection and cursor attributes to None.

        Parameters:
            self (ResumeConnectionHandler): The instance of the ResumeConnectionHandler class.

        Returns:
            None: This method does not return anything.
        """
        if self.connection:
            self.connection.close()
            self.connection = None

        if self.cursor:
            self.cursor.close()
            self.cursor = None


    async def registry_user(self, name: str, password: str) -> Tuple[bool, str]:
        """
            Asynchronously registers a user in the database.

            This method inserts a new row in the "users_data_info" table with the provided name and password.

            Parameters:
                self (ResumeConnectionHandler): The instance of the ResumeConnectionHandler class.
                name (str): The name of the user to be registered.
                password (str): The password of the user to be registered.

            Returns:
                Tuple[bool, str]: A tuple containing a boolean value indicating whether the registration was successful
        """
        query = "INSERT INTO users_data_info (name, password) VALUES (%s, %s)"
        try:
            self.cursor.execute(query, (name, password))
            self.connection.commit()
            return True, "User registered successfully"
        except Exception as error:
            logging.error("Failed to register user.  Error: %s", error)           
            raise HTTPException(
                    status_code=500, 
                    detail=f"Failed to register user.  Error: {error}") from error
    


    async def get_filtered_value(self, field_name: str, field_value: str) -> List[Tuple]:
        """
        Asynchronously retrieves filtered values from the repository based on the given field name and value, with pagination.

        Args:
            field_name (str): The name of the field to filter by.
            field_value (str): The value to filter by.


        Returns:
            List[Tuple]: A list of tuples representing the filtered rows from the 'users_data' table, paginated.
        """
        select_query = f"""
            SELECT * FROM users_data_info
            WHERE {field_name} = '{field_value}'
        """
        try: 
            self.cursor.execute(select_query)
            result = self.cursor.fetchall()
        except Exception as error:
            logging.error("Failed to get filtered value. Error: %s", error)
            raise HTTPException(status_code=500, detail=f"Failed to get filtered value. Error: {error}") from error
        return result
    

    async def login_user(self, name: str, password: str) -> None:
        """
            Asynchronously logs in a user in the database.

            This method retrieves a row from the "users_data_info" table with the provided name and password.

            Parameters:
                self (ResumeConnectionHandler): The instance of the ResumeConnectionHandler class.
                name (str): The name of the user to be logged in.
                password (str): The password of the user to be logged in.

            Returns:
                Tuple[bool, str]: A tuple containing a boolean value indicating whether the login was successful
        """
        user_info = await self.get_filtered_value("name", name)
        if user_info:
            if user_info[0][2] == password:
                return {
                    "name": name,
                    "access_token": await criar_token_jwt(name)
                }
            else:
                raise HTTPException(
                status_code=403, 
                detail=f"Failed to login user.  Error: Password or userName incorrect.")
        else:
           raise HTTPException(
                status_code=404, 
                detail=f"User not found.  Error: User does not exist")
