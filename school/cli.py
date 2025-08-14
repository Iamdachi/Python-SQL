from .config import DB_CONFIG
from .readers import JSONReader
from .db.connection import MySQLConnectionManager
from .db.service import MySQLService
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"

def load_data():
    with MySQLConnectionManager(**DB_CONFIG) as conn:
        service = MySQLService(conn)
        service.run_sql_file(Path(__file__).parent / "db" / "schema.sql")

        reader = JSONReader()

        students = reader.read(DATA_DIR / "students.json")
        rooms = reader.read(DATA_DIR / "rooms.json")

        service.insert_data(rooms)
        service.insert_data(students)

        print(service.get_rooms_with_student_count())
        print(service.get_top5_smallest_avg_age())
        print(service.get_top5_largest_age_diff())
        print(service.get_rooms_with_mixed_sex())
