import sqlite3
import logging

class TriangleDatabase:
    def __init__(self,db_path:str="triangle.db"):
        self.db_path = db_path
        self._init_db()

    def _connec(self):
        return sqlite3.connect(self.db_path)
    def _init_db(self):
        with self.connect() as conn:
            conn.execute("""CREATE TABLE IF NOT EXISTS triangles (
                    side_a REAL NOT NULL,
                    side_b REAL NOT NULL,
                    side_c REAL NOT NULL,
                    triangle_type TEXT NOT NULL,
                    error_message TEXT,
                    PRIMARY KEY (side_a, side_b, side_c)
                )
            """)
        logging.info(f"БД инициализирована:{self.db_path}")

    def add_record(self, a: float, b: float, c: float,
                   triangle_type: str, error_message: str = ""):
        """Добавляет запись. При конфликте — заменяет."""
        with self._connect() as conn:
            conn.execute(
                """INSERT OR REPLACE INTO triangles
                   (side_a, side_b, side_c, triangle_type, error_message)
                   VALUES (?, ?, ?, ?, ?)""",
                (a, b, c, triangle_type, error_message),
            )
        logging.info(f"Запись добавлена: ({a}, {b}, {c}) -> {triangle_type}")

    def get_record(self, a: float, b: float, c: float):
        """Возвращает (triangle_type, error_message) или None."""
        with self._connect() as conn:
            cur = conn.execute(
                """SELECT triangle_type, error_message FROM triangles
                   WHERE side_a = ? AND side_b = ? AND side_c = ?""",
                (a, b, c),
            )
            row = cur.fetchone()
        if row:
            logging.debug(f"Найдена запись для ({a}, {b}, {c}): {row}")
            return row
        logging.debug(f"Запись для ({a}, {b}, {c}) не найдена")
        return None

    def delete_record(self, a: float, b: float, c: float) -> bool:
        """Удаляет запись. Возвращает True, если что-то удалено."""
        with self._connect() as conn:
            cur = conn.execute(
                """DELETE FROM triangles
                   WHERE side_a = ? AND side_b = ? AND side_c = ?""",
                (a, b, c),
            )
            deleted = cur.rowcount > 0
        logging.info(f"Удаление ({a}, {b}, {c}): {deleted}")
        return deleted