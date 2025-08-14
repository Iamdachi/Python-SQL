from pathlib import Path
from typing import Any
from ..models import Student, Room
import mysql.connector

class MySQLService:
    def __init__(self, connection):
        self.conn = connection

    def run_query(self, query: str, params: tuple[Any, ...] = ()) -> list[tuple]:
        with self.conn.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()

    def run_sql_file(self, filepath: Path) -> None:
        with open(filepath, "r", encoding="utf-8") as f:
            sql_commands = f.read()
        with self.conn.cursor() as cursor:
            for _ in cursor.execute(sql_commands, multi=True):
                pass
        self.conn.commit()

    @staticmethod
    def prepare_student_insert_query(data: list[Student]) -> tuple:
        """Prepare a student insert query."""
        query = """
                INSERT INTO students (id, name, birthday, sex, room_id)
                VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY
                UPDATE
                    name =
                VALUES (name), birthday =
                VALUES (birthday), sex =
                VALUES (sex), room_id =
                VALUES (room_id) \
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
        return query, values

    @staticmethod
    def prepare_room_insert_query(data: list[Student]) -> tuple:
        """Prepare a room insert query."""
        query = """
                INSERT INTO rooms (id, name)
                VALUES (%s, %s) ON DUPLICATE KEY
                UPDATE name =
                VALUES (name) \
                """
        values = [(room["id"], room["name"]) for room in data]
        return query, values

    def prepare_insert_query(self, data: list[Student] | list[Room]) -> tuple:
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
        if "room" in first:
            return self.prepare_student_insert_query(data)
        elif "name" in first and "id" in first:
            return self.prepare_room_insert_query(data)
        else:
            raise ValueError("Data format not recognized as Room or Student")

    def insert_data(self, data: list[Student] | list[Room]) -> None:
        """Insert student or room data into the database.

        Args:
            data list[Student] or  list[Room]]: A list of `Student` or `Room` objects to insert.

        Raises:
            mysql.connector.Error: If the insertion fails.
            ValueError: If the provided data type is not supported.
        """
        if not data:
            return

        query, values = self.prepare_insert_query(data)
        with self.conn.cursor() as cursor:
            cursor.executemany(query, values)
            self.conn.commit()

    def get_rooms_with_student_count(self) -> list[tuple]:
        query = """
                SELECT r.id, r.name, COUNT(s.id) AS student_count
                FROM rooms r
                         LEFT JOIN students s ON s.room_id = r.id
                GROUP BY r.id, r.name
                ORDER BY r.id; \
                """
        return self.run_query(query)

    def get_top5_smallest_avg_age(self) -> list[tuple]:
        query = """
                SELECT r.id, \
                       r.name,
                       AVG(TIMESTAMPDIFF(YEAR, s.birthday, CURDATE())) AS avg_age
                FROM rooms r
                         JOIN students s ON s.room_id = r.id
                GROUP BY r.id, r.name
                ORDER BY avg_age ASC LIMIT 5; \
                """
        return self.run_query(query)

    def get_top5_largest_age_diff(self) -> list[tuple]:
        query = """
                SELECT r.id, \
                       r.name,
                       MAX(TIMESTAMPDIFF(YEAR, s.birthday, CURDATE())) -
                       MIN(TIMESTAMPDIFF(YEAR, s.birthday, CURDATE())) AS age_diff
                FROM rooms r
                         JOIN students s ON s.room_id = r.id
                GROUP BY r.id, r.name
                ORDER BY age_diff DESC LIMIT 5; \
                """
        return self.run_query(query)

    def get_rooms_with_mixed_sex(self) -> list[tuple]:
        query = """
                SELECT r.id, r.name
                FROM rooms r
                         JOIN students s ON s.room_id = r.id
                GROUP BY r.id, r.name
                HAVING COUNT(DISTINCT s.sex) > 1; \
                """
        return self.run_query(query)

    def run_sql_file(self, filepath: Path) -> None:
        with open(filepath, "r", encoding="utf-8") as f:
            sql_commands = f.read()
        for command in sql_commands.split(";"):
            command = command.strip()
            if command:
                self.run_query(command)
