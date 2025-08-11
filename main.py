import json
from abc import ABC, abstractmethod
from typing import Any, TypedDict

import mysql.connector
from mysql.connector import MySQLConnection


class Room(TypedDict):
    id: int
    name: str


class Student(TypedDict):
    birthday: str
    id: int
    name: str
    room: int
    sex: str


class ReaderInterface(ABC):
    @abstractmethod
    def read(self, filepath: str) -> list[Student] | list[Room]:
        """Read students or rooms data from a file.

        Args:
            filepath: Path to the file.

        Returns:
            The parsed list of students or rooms.
        """
        pass


class JSONReader(ReaderInterface):
    """Read JSON data from a file."""

    def read(self, filepath: str) -> list[Student] | list[Room]:
        """Read and parse JSON from a file.

        Args:
            filepath: Path to the JSON file.

        Returns:
            The parsed JSON content.
        """
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)


class MySQLConnectionManager:
    """Manages MySQL connections."""
    def __init__(self, host: str, user: str, password: str, database: str):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self._conn: MySQLConnection | None = None

    def __enter__(self) -> MySQLConnection:
        self._conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        return self._conn

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self._conn:
            self._conn.close()


class MySQLService:
    """Encapsulates database operations."""
    def __init__(self, connection: MySQLConnection):
        """Initialize the database service with a MySQL connection.

        Args:
            connection (MySQLConnection): An active MySQL database connection.
        """

        self.conn = connection

    def run_query(self, query: str, params: tuple[Any, ...] = ()) -> list[tuple]:
        """Execute a SQL query and return the results.

        Args:
            query (str): The SQL query string to execute.
            params (tuple[Any, ...], optional): Parameters to bind to the query.
                Defaults to an empty tuple.

        Returns:
            list[tuple]: The fetched rows from the query result.
        """
        with self.conn.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()

    @staticmethod
    def prepare_query(data: list[Student] | list[Room]) -> tuple:
        """Prepare an SQL INSERT query and corresponding values.

        Args:
            data (list[Student] | list[Room]): List of `Student` or `Room` objects.

        Returns:
            tuple: A tuple containing:
                - str: SQL query string with placeholders.
                - list[tuple]: Values to insert, as a list of tuples.

        Raises:
            ValueError: If the data type is not supported.
        """

        # Check if data is rooms or students by keys
        first = data[0]
        query = """"""
        values = []
        if "room" in first:
            # It's Student data
            query = """
                    INSERT INTO students (id, name, birthday, sex, room_id)
                    VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY 
                    UPDATE 
                        name = 
                    VALUES (name), birthday =
                    VALUES (birthday), sex =
                    VALUES (sex), room_id =
                    VALUES (room_id)
                    """
            values = [
                (
                    student["id"],
                    student["name"],
                    student["birthday"][:10],  # YYYY-MM-DD from ISO datetime string
                    student["sex"],
                    student["room"],
                )
                for student in data
            ]
        elif "name" in first and "id" in first:
            # It's Room data
            query = """
                    INSERT INTO rooms (id, name)
                    VALUES (%s, %s) ON DUPLICATE KEY 
                    UPDATE name = 
                    VALUES (name) 
                    """
            values = [(room["id"], room["name"]) for room in data]
        else:
            raise ValueError("Data format not recognized as Room or Student")
        return query, values

    def insert_data(self, data: list[Student] | list[Room]) -> None:
        """Insert student or room data into the database.

        Args:
            data list[Student] or  list[Room]]: A list of `Student` or `Room` objects to insert.

        Raises:
            mysql.connector.Error: If the insertion fails.
            ValueError: If the provided data type is not supported.
        """
        if not data:
            return  # nothing to insert

        query, values = self.prepare_query(data)
        with self.conn.cursor() as cursor:
            cursor.executemany(query, values)
            self.conn.commit()


def main() -> None:
    """Main entry point for loading data into the MySQL database.

    This function:
        - Establishes a connection to the MySQL database using configuration
          parameters.
        - Reads student and room data from JSON files.
        - Inserts the data into the database.

    The database connection is managed using a context manager, ensuring
    that it is closed automatically.

    Raises:
        mysql.connector.Error: If there is a problem connecting to or
            interacting with the MySQL database.
        FileNotFoundError: If the JSON input files do not exist.
        json.JSONDecodeError: If the JSON files contain invalid data.
        """
    # Configuration could be loaded from env/config file
    db_config = {
        "host": "127.0.0.1",
        "user": "root",
        "password": "",
        "database": "mysql"
    }

    with MySQLConnectionManager(**db_config) as conn:
        service = MySQLService(conn)
        #version = service.run_query("SELECT VERSION();")
        #print("MySQL version:", version[0][0])

        service.run_query("use school;")
        reader = JSONReader()
        students = reader.read("students.json")
        rooms = reader.read("rooms.json")

        service.insert_data(rooms)
        service.insert_data(students)


if __name__ == "__main__":
    main()
