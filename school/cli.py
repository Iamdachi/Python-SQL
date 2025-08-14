from pathlib import Path

from school.config import DB_CONFIG
from school.readers import JSONReader
from school.db.connection import MySQLConnectionManager
from school.db.service import MySQLService

DATA_DIR = Path(__file__).parent / "data"


def load_data():
    """Load schema, rooms, and students from JSON files into the database."""
    with MySQLConnectionManager(**DB_CONFIG) as conn:
        service = MySQLService(conn)
        service.run_sql_file(Path(__file__).parent / "db" / "schema.sql")

        if service.db_not_indexed():
            service.run_sql_file(Path(__file__).parent / "db" / "indexing.sql")

        reader = JSONReader()

        students = reader.read(DATA_DIR / "students.json")
        rooms = reader.read(DATA_DIR / "rooms.json")

        service.insert_data(rooms)
        service.insert_data(students)

        print(service.get_rooms_with_student_count())
        print(service.get_top5_smallest_avg_age())
        print(service.get_top5_largest_age_diff())
        print(service.get_rooms_with_mixed_sex())
